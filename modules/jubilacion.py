import streamlit as st
import plotly.graph_objects as go
from utils.calculos import calcular_pension_mensual, calcular_impuesto
import plotly.io as pio
import io

def mostrar_modulo_jubilacion():
    st.header("💰 Módulo B: Proyección de Jubilación")
    st.markdown("---")
    
    with st.expander("ℹ️ Ayuda - ¿Cómo usar esta calculadora?"):
        st.write("""
        Este módulo calcula tu pensión mensual considerando:
        - **Capital acumulado**: Del módulo A o ingresado manualmente
        - **Impuestos**: Según el origen de las ganancias
        - **Años de retiro**: Cuánto durará tu jubilación
        - **Pensión mensual**: Cuánto recibirás cada mes
        """)
    
    if 'cartera_saldo_final' not in st.session_state:
        st.warning("⚠️ Primero calcula tu cartera en el Módulo A, o ingresa un capital manualmente")
        usar_manual = True
    else:
        usar_manual = st.checkbox(
            "Usar capital manual (ignorar Módulo A)",
            help="Marca esta opción si quieres ingresar un capital diferente"
        )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💼 Capital Disponible")
        
        if usar_manual:
            capital_acumulado = st.number_input(
                "Capital Acumulado (USD)",
                min_value=0.0,
                value=100000.0,
                step=1000.0,
                help="Capital total que tienes al momento de jubilarte"
            )
            
            total_aportes = st.number_input(
                "Total Aportado (USD)",
                min_value=0.0,
                value=50000.0,
                step=1000.0,
                help="Suma de todo lo que aportaste (para calcular ganancia)"
            )
        else:
            capital_acumulado = st.session_state['cartera_saldo_final']
            total_aportes = st.session_state['cartera_total_aportes']
            st.info(f"💰 Capital del Módulo A: ${capital_acumulado:,.2f}")
            st.info(f"📊 Total Aportado: ${total_aportes:,.2f}")
        
        tipo_impuesto = st.selectbox(
            "Tipo de Inversión",
            ["extranjera", "local"],
            format_func=lambda x: "Fuente Extranjera (29.5%)" if x == "extranjera" else "Bolsa Local (5%)",
            help="Selecciona el tipo de inversión para calcular impuestos"
        )
    
    with col2:
        st.subheader("⚙️ Parámetros de Retiro")
        
        opcion_retiro = st.radio(
            "Opción de Retiro",
            ["Pensión Mensual", "Cobro Total"],
            help="Elige cómo quieres recibir tu dinero"
        )
        
        if opcion_retiro == "Pensión Mensual":
            anos_retiro = st.number_input(
                "Años de Retiro",
                min_value=1,
                max_value=50,
                value=20,
                help="Durante cuántos años recibirás pensión"
            )
            
            tea_retiro = st.number_input(
                "TEA durante Retiro (%)",
                min_value=0.0,
                max_value=50.0,
                value=5.0,
                step=0.5,
                help="Rentabilidad esperada durante la jubilación"
            )
        else:
            anos_retiro = None
            tea_retiro = None
    
    st.markdown("---")
    
    if st.button("💵 Calcular Jubilación", type="primary", use_container_width=True):
        ganancia = capital_acumulado - total_aportes
        
        if ganancia < 0:
            st.error("❌ El capital acumulado no puede ser menor que el total aportado")
            return
        
        impuesto = calcular_impuesto(ganancia, tipo_impuesto)
        capital_neto = capital_acumulado - impuesto
        
        if opcion_retiro == "Pensión Mensual":
            pension_mensual = calcular_pension_mensual(capital_neto, tea_retiro, anos_retiro)
        else:
            pension_mensual = 0
        
        st.session_state['jubilacion_data'] = {
            'capital_bruto': capital_acumulado,
            'total_aportes': total_aportes,
            'ganancia': ganancia,
            'impuesto': impuesto,
            'capital_neto': capital_neto,
            'pension_mensual': pension_mensual,
            'tipo_impuesto': tipo_impuesto,
            'opcion_retiro': opcion_retiro,
            'anos_retiro': anos_retiro,
            'tea_retiro': tea_retiro
        }
        
        st.success("✅ Cálculo de jubilación completado")
    
    if 'jubilacion_data' in st.session_state:
        st.markdown("---")
        st.subheader("📊 Resultados de Jubilación")
        
        data = st.session_state['jubilacion_data']
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Capital Bruto", f"${data['capital_bruto']:,.2f}")
        col2.metric("Impuesto", f"${data['impuesto']:,.2f}", delta=f"-{(data['impuesto']/data['capital_bruto']*100):.1f}%")
        col3.metric("Capital Neto", f"${data['capital_neto']:,.2f}")
        
        if data['opcion_retiro'] == "Pensión Mensual":
            st.markdown("---")
            st.success(f"### 💵 Pensión Mensual: ${data['pension_mensual']:,.2f}")
            st.info(f"Recibirás esta pensión durante {data['anos_retiro']} años ({data['anos_retiro'] * 12} meses)")
            
            fig = go.Figure()
            
            meses = list(range(1, data['anos_retiro'] * 12 + 1))
            pension_acumulada = [data['pension_mensual'] * i for i in meses]
            
            fig.add_trace(go.Scatter(
                x=meses,
                y=pension_acumulada,
                mode='lines',
                name='Pensión Acumulada',
                line=dict(color='#00CC96', width=3),
                fill='tozeroy'
            ))
            
            fig.add_hline(
                y=data['capital_neto'],
                line_dash="dash",
                line_color="red",
                annotation_text=f"Capital Inicial: ${data['capital_neto']:,.0f}"
            )
            
            fig.update_layout(
                title='Proyección de Retiro Mensual',
                xaxis_title='Mes',
                yaxis_title='Monto Acumulado (USD)',
                template='plotly_white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Guardar imagen para reporte con manejo de errores robusto
            try:
                img_bytes = io.BytesIO()
                fig.write_image(img_bytes, format="png", width=1200, height=600)
                img_bytes.seek(0)
                st.session_state['jubilacion_grafico'] = img_bytes.getvalue()
            except Exception as e:
                # Fallback: intentar con matplotlib
                try:
                    import matplotlib.pyplot as plt
                    import matplotlib
                    matplotlib.use('Agg')
                    
                    fig_mpl, ax = plt.subplots(figsize=(12, 6))
                    ax.plot(meses, pension_acumulada, linewidth=3, color='#00CC96')
                    ax.fill_between(meses, 0, pension_acumulada, alpha=0.3, color='#00CC96')
                    ax.axhline(y=data['capital_neto'], linestyle='--', color='red', 
                              label=f"Capital Inicial: ${data['capital_neto']:,.0f}")
                    ax.set_xlabel('Mes', fontsize=12)
                    ax.set_ylabel('Monto Acumulado (USD)', fontsize=12)
                    ax.set_title('Proyección de Retiro Mensual', fontsize=14, fontweight='bold')
                    ax.legend(fontsize=10)
                    ax.grid(True, alpha=0.3)
                    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
                    
                    img_bytes = io.BytesIO()
                    plt.savefig(img_bytes, format='png', dpi=150, bbox_inches='tight')
                    img_bytes.seek(0)
                    st.session_state['jubilacion_grafico'] = img_bytes.getvalue()
                    plt.close()
                except Exception as e2:
                    # Si ambos fallan, no guardar imagen pero continuar
                    st.session_state['jubilacion_grafico'] = None

        else:
            st.success(f"### 💰 Cobro Total: ${data['capital_neto']:,.2f}")
            st.info("Recibirás todo el dinero en un solo pago")
        
        with st.expander("📋 Comparar Escenarios"):
            st.subheader("Comparación de Edades de Retiro")
            
            edades = [60, 62, 65, 68, 70]
            pensiones = []
            
            for edad in edades:
                anos = edad - 30
                capital_futuro = data['capital_neto'] * (1 + data.get('tea_retiro', 5)/100) ** (edad - 65)
                pension = calcular_pension_mensual(capital_futuro, data.get('tea_retiro', 5), 20)
                pensiones.append(pension)
            
            fig_comp = go.Figure()
            fig_comp.add_trace(go.Bar(
                x=[f"{e} años" for e in edades],
                y=pensiones,
                marker_color='lightblue'
            ))
            
            fig_comp.update_layout(
                title='Pensión Mensual según Edad de Retiro',
                xaxis_title='Edad de Jubilación',
                yaxis_title='Pensión Mensual (USD)',
                template='plotly_white'
            )
            
            st.plotly_chart(fig_comp, use_container_width=True)
