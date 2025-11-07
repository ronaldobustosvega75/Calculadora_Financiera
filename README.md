# 💰 Calculadora Financiera - Finanzas Corporativas

Aplicación web interactiva para proyección de inversiones, cálculo de jubilación y valoración de bonos.

## 🚀 Instalación

### Opción 1: Ejecución Directa (Python)

```bash
# Clonar o descargar el proyecto
cd calculadora_financiera

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
streamlit run app.py
```
## 📦 Estructura del Proyecto

```
calculadora_financiera/
├── app.py                  # Aplicación principal
├── requirements.txt        # Dependencias
├── modules/               # Módulos funcionales
│   ├── cartera.py         # Crecimiento de cartera
│   ├── jubilacion.py      # Proyección de jubilación
│   └── bonos.py           # Valoración de bonos
├── utils/                 # Utilidades
│   ├── calculos.py        # Cálculos financieros
│   ├── validaciones.py    # Validaciones
│   └── exportar.py        # Exportación PDF


## 🎯 Módulos

### 📊 Módulo A: Crecimiento de Cartera
- Cálculo de crecimiento con interés compuesto
- Aportes periódicos (mensual, trimestral, semestral, anual)
- Gráficas de evolución
- Proyección a largo plazo

### 💰 Módulo B: Proyección de Jubilación
- Cálculo de pensión mensual
- Consideración de impuestos (5% local, 29.5% extranjera)
- Opción de cobro total o pensión mensual
- Comparación de escenarios

### 📈 Módulo C: Valoración de Bonos
- Cálculo de valor presente
- Análisis de flujos de caja
- Múltiples frecuencias de pago
- Análisis de sensibilidad

## 🛠️ Tecnologías

- **Python 3.9+**
- **Streamlit**: Framework web
- **Pandas**: Manipulación de datos
- **Plotly**: Gráficas interactivas
- **ReportLab**: Generación de PDFs

## 👥 Equipo de Desarrollo

- **TAKESHY**: Integración y coordinación
- **ADRIAN**: Módulo de Cartera
- **ROBLES**: Módulo de Jubilación
- **SAMIRA**: Módulo de Bonos
- **BUSTOS**: Utilidades y exportación

## 📝 Uso Rápido

1. Ejecutar la aplicación
2. Seleccionar un módulo en el menú lateral
3. Ingresar los datos requeridos
4. Hacer clic en "Calcular"
5. Ver resultados y gráficas
6. Exportar a PDF si es necesario


## 📧 Soporte

Para dudas o problemas, contactar al equipo de desarrollo.

## 📄 Licencia

Proyecto académico 
