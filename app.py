import streamlit as st
from modules.cartera import mostrar_modulo_cartera
from modules.jubilacion import mostrar_modulo_jubilacion
from modules.bonos import mostrar_modulo_bonos
from utils.exportar import generar_pdf_reporte

st.set_page_config(
    page_title="Calculadora Financiera",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
    }
    h1 {
        color: #1f77b4;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("💰 Calculadora Financiera")
    st.markdown("---")
    
    pagina = st.radio(
        "Selecciona un módulo:",
        ["🏠 Inicio", "📊 Cartera", "💰 Jubilación", "📈 Bonos", "📄 Exportar"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 📚 Guía Rápida")
    st.write("""
    1. **Cartera**: Proyecta tu inversión
    2. **Jubilación**: Calcula tu pensión
    3. **Bonos**: Valora instrumentos
    4. **Exportar**: Descarga reporte
    """)
    
    st.markdown("---")
    st.caption("Desarrollado para Finanzas Corporativas")
    st.caption("© 2024 - Todos los derechos reservados")

if pagina == "🏠 Inicio":
    st.title("🏠 Bienvenido a tu Calculadora Financiera")
    st.markdown("---")
    
    st.markdown("""
    ### 🎯 ¿Qué puedes hacer con esta aplicación?
    
    Esta herramienta te permite planificar tu futuro financiero de manera profesional y sencilla.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Módulo Cartera</h3>
            <p>Proyecta cómo crecerá tu inversión con aportes periódicos y interés compuesto</p>
            <ul>
                <li>Aportes iniciales y periódicos</li>
                <li>Gráficas de crecimiento</li>
                <li>Proyecciones a largo plazo</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>💰 Módulo Jubilación</h3>
            <p>Calcula tu pensión mensual al jubilarte considerando impuestos</p>
            <ul>
                <li>Cálculo de impuestos</li>
                <li>Pensión mensual estimada</li>
                <li>Comparación de escenarios</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>📈 Módulo Bonos</h3>
            <p>Valora bonos y analiza sus flujos de caja descontados</p>
            <ul>
                <li>Valor presente de bonos</li>
                <li>Análisis de flujos</li>
                <li>Sensibilidad de tasas</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("👈 Usa el menú lateral para comenzar con cualquier módulo")
    
    st.markdown("---")
    st.subheader("🚀 Ejemplo Rápido")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Escenario de ejemplo:**
        - Edad actual: 30 años
        - Inversión inicial: $5,000
        - Aporte mensual: $500
        - TEA esperada: 8%
        - Edad de jubilación: 65 años
        """)
    
    with col2:
        st.markdown("""
        **Resultado esperado:**
        - Plazo: 35 años
        - Total aportado: ~$215,000
        - Capital acumulado: ~$1,100,000
        - Pensión mensual: ~$8,500/mes
        """)
    
    st.success("💡 ¡Estos resultados son aproximados! Usa los módulos para cálculos exactos.")

elif pagina == "📊 Cartera":
    mostrar_modulo_cartera()

elif pagina == "💰 Jubilación":
    mostrar_modulo_jubilacion()

elif pagina == "📈 Bonos":
    mostrar_modulo_bonos()

elif pagina == "📄 Exportar":
    st.header("📄 Exportar Reporte Profesional")
    st.markdown("---")
    
    st.info("📋 Genera un reporte PDF con todos tus cálculos, gráficos y análisis financiero detallado.")
    
    tiene_datos = False
    datos_incluir = []
    
    # Verificar disponibilidad segura
    cartera_ok = 'cartera_saldo_final' in st.session_state and 'cartera_params' in st.session_state
    jubilacion_ok = 'jubilacion_data' in st.session_state
    bono_ok = 'bono_vp' in st.session_state and 'bono_params' in st.session_state
    
    if cartera_ok:
        st.success("✅ Datos de Cartera disponibles")
        datos_incluir.append("Cartera")
        tiene_datos = True
    else:
        st.warning("⚠️ Datos incompletos de Cartera — requiere ejecutar el cálculo nuevamente")
    
    if jubilacion_ok:
        st.success("✅ Datos de Jubilación disponibles")
        datos_incluir.append("Jubilación")
        tiene_datos = True
    else:
        st.warning("⚠️ Datos incompletos de Jubilación — requiere ejecutar el cálculo nuevamente")
    
    if bono_ok:
        st.success("✅ Datos de Bonos disponibles")
        datos_incluir.append("Bonos")
        tiene_datos = True
    else:
        st.warning("⚠️ Datos incompletos de Bonos — requiere ejecutar el cálculo nuevamente")
    
    st.markdown("---")
    
    if tiene_datos:
        st.write(f"**Secciones a incluir:** {', '.join(datos_incluir)}")
        
        if st.button("📥 Generar y Descargar PDF", type="primary", use_container_width=True):
            with st.spinner("📊 Generando reporte profesional..."):
                try:
                    # === CARGAR DATOS DE CARTERA ===
                    datos_cartera = None
                    if cartera_ok:
                        p = st.session_state['cartera_params']
                        datos_cartera = {
                            'monto_inicial': p.get('monto_inicial', 0.0),
                            'aporte_periodico': p.get('aporte_periodico', 0.0),
                            'tea': p.get('tea', 0.0),
                            'anos': p.get('anos', 0),
                            'frecuencia': p.get('frecuencia', 'Mensual'),
                            'saldo_final': st.session_state.get('cartera_saldo_final', 0.0),
                            'total_aportes': st.session_state.get('cartera_total_aportes', 0.0)
                        }
                        # Incluir df y gráfico si existen
                        if 'cartera_df' in st.session_state:
                            datos_cartera['df'] = st.session_state['cartera_df']
                        if 'cartera_grafico' in st.session_state:
                            datos_cartera['grafico'] = st.session_state['cartera_grafico']
                
                    # === CARGAR DATOS DE JUBILACIÓN ===
                    datos_jubilacion = None
                    if jubilacion_ok:
                        datos_jubilacion = st.session_state['jubilacion_data'].copy()
                        if 'jubilacion_grafico' in st.session_state:
                            datos_jubilacion['grafico'] = st.session_state['jubilacion_grafico']
                        # Nota: jubilación no usa 'df' actualmente, pero si lo agregas, aquí va
                
                    # === CARGAR DATOS DE BONOS ===
                    datos_bono = None
                    if bono_ok:
                        p = st.session_state['bono_params']
                        datos_bono = {
                            'valor_nominal': p.get('valor_nominal', 1000.0),
                            'tasa_cupon': p.get('tasa_cupon', 0.0),
                            'frecuencia_pago': p.get('frecuencia_pago', 'Anual'),
                            'anos': p.get('anos', 10),
                            'tea_mercado': p.get('tea_mercado', 0.0),
                            'vp_total': st.session_state.get('bono_vp', 0.0)
                        }
                        if 'bono_df' in st.session_state:
                            datos_bono['df'] = st.session_state['bono_df']
                        if 'bono_grafico' in st.session_state:
                            datos_bono['grafico'] = st.session_state['bono_grafico']
                
                    # ✅ AHORA SÍ: Llamar al generador de PDF
                    pdf_buffer = generar_pdf_reporte(
                        datos_cartera, 
                        datos_jubilacion, 
                        datos_bono
                    )
                    
                    st.download_button(
                        label="📄 Descargar Reporte PDF",
                        data=pdf_buffer,
                        file_name="Reporte_Financiero_Integral.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    
                    st.success("✅ ¡Reporte generado con éxito!")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"❌ Error al generar el PDF: {type(e).__name__}")
                    st.code(str(e))
                    st.warning("💡 Recomendación: Ejecuta nuevamente los cálculos en cada módulo y luego intenta exportar.")
    else:
        st.error("❌ No hay datos completos para exportar")
        st.info("📌 Ve a los módulos (📊 Cartera, 💰 Jubilación, 📈 Bonos), ejecuta los cálculos y regresa aquí.")
