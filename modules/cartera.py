import streamlit as st
import plotly.graph_objects as go
from utils.calculos import calcular_crecimiento_cartera
from utils.validaciones import validar_monto, validar_tea, validar_anos
import io

def mostrar_modulo_cartera():
    st.header("📊 Módulo A: Crecimiento de Cartera")
    st.markdown("---")
    
    with st.expander("ℹ️ Ayuda - ¿Cómo usar esta calculadora?"):
        st.write("""
        Este módulo calcula cómo crece tu inversión a lo largo del tiempo considerando:
        - **Monto inicial**: Capital que tienes ahora
        - **Aportes periódicos**: Dinero que agregarás regularmente
        - **TEA**: Tasa de interés anual esperada
        - **Plazo**: Años que mantendrás la inversión
        """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Datos de Inversión")
        
        monto_inicial = st.number_input(
            "Monto Inicial (USD)",
            min_value=0.0,
            value=1000.0,
            step=100.0,
            help="Capital inicial que vas a invertir"
        )
        
        aporte_periodico = st.number_input(
            "Aporte Periódico (USD)",
            min_value=0.0,
            value=100.0,
            step=50.0,
            help="Cantidad que aportarás en cada periodo"
        )
        
        frecuencia = st.selectbox(
            "Frecuencia de Aportes",
            ["Mensual", "Trimestral", "Semestral", "Anual"],
            help="Con qué frecuencia realizarás los aportes"
        )
    
    with col2:
        st.subheader("⚙️ Parámetros")
        
        tea = st.number_input(
            "TEA - Tasa Efectiva Anual (%)",
            min_value=0.0,
            max_value=50.0,
            value=8.0,
            step=0.5,
            help="Rentabilidad anual esperada"
        )
        
        tipo_plazo = st.radio(
            "Definir plazo por:",
            ["Años", "Edad de Jubilación"]
        )
        
        if tipo_plazo == "Años":
            anos = st.number_input(
                "Plazo (años)",
                min_value=1,
                max_value=80,
                value=30,
                help="Años que mantendrás la inversión"
            )
        else:
            col_edad1, col_edad2 = st.columns(2)
            with col_edad1:
                edad_actual = st.number_input("Edad Actual", min_value=18, max_value=90, value=30)
            with col_edad2:
                edad_jubilacion = st.number_input("Edad Jubilación", min_value=18, max_value=100, value=65)
            anos = edad_jubilacion - edad_actual
            st.info(f"Plazo calculado: {anos} años")
    
    st.markdown("---")
    
    if st.button("🚀 Calcular Proyección", type="primary", use_container_width=True):
        if not all([validar_monto(monto_inicial, "Monto inicial"),
                   validar_monto(aporte_periodico, "Aporte periódico"),
                   validar_tea(tea),
                   validar_anos(anos)]):
            return
        
        frecuencias = {"Mensual": 12, "Trimestral": 4, "Semestral": 2, "Anual": 1}
        periodos_anuales = frecuencias[frecuencia]
        periodos_totales = anos * periodos_anuales
        
        df, saldo_final, total_aportes = calcular_crecimiento_cartera(
            monto_inicial, aporte_periodico, tea, periodos_totales, periodos_anuales
        )
        
        st.session_state['cartera_df'] = df
        st.session_state['cartera_saldo_final'] = saldo_final
        st.session_state['cartera_total_aportes'] = total_aportes
        st.session_state['cartera_params'] = {
            'monto_inicial': monto_inicial,
            'aporte_periodico': aporte_periodico,
            'tea': tea,
            'anos': anos,
            'frecuencia': frecuencia
        }
        
        st.success("✅ Cálculo completado exitosamente")
    
    if 'cartera_saldo_final' in st.session_state:
        st.markdown("---")
        st.subheader("📈 Resultados")
        
        ganancia = st.session_state['cartera_saldo_final'] - st.session_state['cartera_total_aportes']
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Aportado", f"${st.session_state['cartera_total_aportes']:,.2f}")
        col2.metric("Ganancia", f"${ganancia:,.2f}")
        col3.metric("Saldo Final", f"${st.session_state['cartera_saldo_final']:,.2f}")
        
        st.subheader("📊 Gráfica de Crecimiento")
        
        df = st.session_state['cartera_df']
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['Periodo'],
            y=df['Total Aportes'],
            mode='lines',
            name='Aportes Acumulados',
            line=dict(color='#636EFA', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=df['Periodo'],
            y=df['Saldo'],
            mode='lines',
            name='Saldo Total',
            line=dict(color='#00CC96', width=3),
            fill='tonexty'
        ))
        
        fig.update_layout(
            title='Evolución de la Inversión',
            xaxis_title='Periodo',
            yaxis_title='Monto (USD)',
            hovermode='x unified',
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Guardar imagen para reporte con manejo de errores robusto
        try:
            img_bytes = io.BytesIO()
            fig.write_image(img_bytes, format="png", width=1200, height=600)
            img_bytes.seek(0)
            st.session_state['cartera_grafico'] = img_bytes.getvalue()
        except Exception as e:
            # Fallback: intentar con matplotlib
            try:
                import matplotlib.pyplot as plt
                import matplotlib
                matplotlib.use('Agg')
                
                fig_mpl, ax = plt.subplots(figsize=(12, 6))
                ax.plot(df['Periodo'], df['Total Aportes'], label='Aportes Acumulados', 
                        linewidth=2, color='#636EFA')
                ax.plot(df['Periodo'], df['Saldo'], label='Saldo Total', 
                        linewidth=3, color='#00CC96')
                ax.fill_between(df['Periodo'], df['Total Aportes'], df['Saldo'], 
                                alpha=0.3, color='#00CC96')
                ax.set_xlabel('Periodo', fontsize=12)
                ax.set_ylabel('Monto (USD)', fontsize=12)
                ax.set_title('Evolución de la Inversión', fontsize=14, fontweight='bold')
                ax.legend(fontsize=10)
                ax.grid(True, alpha=0.3)
                ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
                
                img_bytes = io.BytesIO()
                plt.savefig(img_bytes, format='png', dpi=150, bbox_inches='tight')
                img_bytes.seek(0)
                st.session_state['cartera_grafico'] = img_bytes.getvalue()
                plt.close()
            except Exception as e2:
                # Si ambos fallan, no guardar imagen pero continuar
                st.session_state['cartera_grafico'] = None
                # No mostrar warning aquí para no confundir al usuario
        
        with st.expander("📋 Ver Tabla Detallada"):
            st.dataframe(df, use_container_width=True, hide_index=True)
