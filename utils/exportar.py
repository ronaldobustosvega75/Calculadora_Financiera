# utils/exportar.py (reemplaza tu versión actual)
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph,
    Spacer, PageBreak, Image, KeepTogether, Frame, PageTemplate
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import io
import pandas as pd
import base64

def generar_pdf_reporte(datos_cartera, datos_jubilacion, datos_bono=None):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=50, leftMargin=50,
        topMargin=50, bottomMargin=50
    )
    elements = []
    styles = getSampleStyleSheet()

    # ======== ESTILOS PERSONALIZADOS (mejorados) ========
    title_style = ParagraphStyle(
        'CustomTitle',
        fontSize=26,
        textColor=colors.HexColor('#0D4A6B'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        leading=32
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        fontSize=11,
        textColor=colors.HexColor('#6C757D'),
        alignment=TA_CENTER,
        spaceAfter=20,
        fontName='Helvetica'
    )
    
    section_style = ParagraphStyle(
        'SectionTitle',
        fontSize=15,
        textColor=colors.white,
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold',
        backColor=colors.HexColor('#0D4A6B'),
        borderPadding=(10, 8),
        alignment=TA_LEFT
    )
    
    insight_style = ParagraphStyle(
        'InsightBox',
        fontSize=10,
        textColor=colors.HexColor('#1F2937'),
        backColor=colors.HexColor('#F0F9FF'),
        borderColor=colors.HexColor('#E0F2FE'),
        borderWidth=1,
        borderPadding=(10, 8),
        borderRadius=6,
        spaceAfter=15,
        fontName='Helvetica',
        leading=14
    )
    
    description_style = ParagraphStyle(
        'Description',
        fontSize=10,
        textColor=colors.HexColor('#374151'),
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        fontName='Helvetica',
        leading=14
    )

    # ======== PORTADA ========
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("📊 REPORTE FINANCIERO INTEGRAL", title_style))
    elements.append(Paragraph(
        f"<b>Análisis de Cartera, Jubilación y Valoración de Bonos</b><br/>"
        f"Generado el <b>{datetime.now().strftime('%d de %B de %Y')}</b> a las <b>{datetime.now().strftime('%H:%M')}</b>",
        subtitle_style
    ))
    
    # Línea de firma
    line_data = [['']]
    line_table = Table(line_data, colWidths=[6.5*inch])
    line_table.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 2, colors.HexColor('#0D4A6B')),
        ('TOPPADDING', (0,0), (-1,0), 10),
    ]))
    elements.append(line_table)
    elements.append(Spacer(1, 0.3*inch))

    elements.append(Paragraph(
        "Este documento presenta un análisis cuantitativo y cualitativo de tus proyecciones financieras, "
        "diseñado para apoyar la toma de decisiones estratégicas con base en principios de finanzas modernas.",
        description_style
    ))
    elements.append(Spacer(1, 0.4*inch))

    # ======== RESUMEN EJECUTIVO (si hay datos) ========
    resumen_items = []
    if datos_cartera:
        resumen_items.append(f"• Cartera: <b>${datos_cartera['saldo_final']:,.0f}</b> en {datos_cartera['anos']} años")
    if datos_jubilacion:
        resumen_items.append(f"• Jubilación: pensión de <b>${datos_jubilacion['pension_mensual']:,.0f}/mes</b>")
    if datos_bono:
        diff_pct = (datos_bono['vp_total'] - datos_bono['valor_nominal']) / datos_bono['valor_nominal'] * 100
        estado = "sobrevaluado" if diff_pct > 0 else "subvaluado" if diff_pct < 0 else "a la par"
        resumen_items.append(f"• Bono: valor presente <b>${datos_bono['vp_total']:,.0f}</b> ({estado})")

    if resumen_items:
        elements.append(Paragraph("<b>🔍 Resumen Ejecutivo</b>", section_style))
        resumen_texto = "<br/>".join(resumen_items)
        elements.append(Paragraph(resumen_texto, description_style))
        elements.append(Spacer(1, 0.3*inch))

    # ======== MÓDULO A: CARTERA ========
    if datos_cartera:
        elements.append(Paragraph("📈 MÓDULO 1: PROYECCIÓN DE CRECIMIENTO DE CARTERA", section_style))
        
        # Contexto
        elements.append(Paragraph(
            "Esta sección modela el crecimiento de tu inversión mediante <b>capitalización compuesta</b>. "
            "El rendimiento final depende no solo de la tasa de interés, sino también de la disciplina en "
            "los aportes periódicos y del horizonte temporal —el mayor aliado del interés compuesto.",
            description_style
        ))

        # Tabla resumen (mejorada)
        total_aportes = datos_cartera['total_aportes']
        ganancia = datos_cartera['saldo_final'] - total_aportes
        rentabilidad = (ganancia / total_aportes * 100) if total_aportes > 0 else 0
        
        resumen_cartera = [
            ['Parámetro', 'Valor'],
            ['Inversión Inicial', f"${datos_cartera['monto_inicial']:,.2f}"],
            ['Aporte Mensual', f"${datos_cartera['aporte_periodico']:,.2f}"],
            ['Plazo', f"{datos_cartera['anos']} años ({datos_cartera['anos']*12} meses)"],
            ['TEA', f"{datos_cartera['tea']:.2f}%"],
            ['Total Aportado', f"${total_aportes:,.2f}"],
            ['Ganancia Neta', f"${ganancia:,.2f} ({rentabilidad:+.1f}%)"],
            ['<b>SALDO FINAL</b>', f"<b>${datos_cartera['saldo_final']:,.2f}</b>"],
        ]
        
        t_resumen = Table(resumen_cartera, colWidths=[3*inch, 2.8*inch])
        t_resumen.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E3F2FD')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#0D4A6B')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 10),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,1), (-1,-1), 9),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BBDEFB')),
            ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#BBDEFB')),
            ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0,-1), (-1,-1), colors.HexColor('#0D4A6B')),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        elements.append(t_resumen)
        elements.append(Spacer(1, 0.2*inch))

        # Insight
        if rentabilidad > 100:
            insight = (
                "<b>💡 Hallazgo clave:</b> Más del 50% de tu capital final proviene del interés compuesto, "
                "no de tus aportes. Esto ilustra el poder de comenzar temprano y mantener la disciplina."
            )
        else:
            insight = (
                "<b>🔍 Observación:</b> Aumentar el plazo o la tasa de retorno tendría un impacto exponencial. "
                "Por ejemplo, extender 5 años más podría incrementar tu saldo final en +25%."
            )
        elements.append(Paragraph(insight, insight_style))
        elements.append(Spacer(1, 0.2*inch))

        # Gráfico
        if 'grafico' in datos_cartera and datos_cartera['grafico']:
            try:
                img = Image(io.BytesIO(datos_cartera['grafico']), width=6.2*inch, height=2.8*inch)
                elements.append(Paragraph("Evolución del Capital (Aportes vs Intereses)", description_style))
                elements.append(img)
                elements.append(Spacer(1, 0.2*inch))
            except Exception as e:
                elements.append(Paragraph(f"<i>⚠️ Error al cargar gráfico: {str(e)}</i>", description_style))

        # Tabla detallada de flujos (si existe df)
        if 'df' in datos_cartera and isinstance(datos_cartera['df'], pd.DataFrame) and not datos_cartera['df'].empty:
            elements.append(Paragraph("Detalle de los Primeros y Últimos Periodos", description_style))
            
            df = datos_cartera['df']
            if len(df) > 12:
                df_show = pd.concat([df.head(6), df.tail(6)])
                omitidos = len(df) - 12
            else:
                df_show = df
                omitidos = 0
            
            # Formatear tabla
            data = [['Periodo', 'Aporte', 'Interés', 'Saldo Acumulado']]
            for _, r in df_show.iterrows():
                data.append([
                    str(int(r['Periodo'])),
                    f"${r['Aporte']:,.0f}",
                    f"${r['Interes']:,.0f}",
                    f"${r['Saldo']:,.0f}"
                ])
            
            if omitidos > 0:
                data.insert(7, ['…', '…', '…', '…'])
            
            t_detalle = Table(data, colWidths=[1*inch, 1.7*inch, 1.7*inch, 2.4*inch])
            t_detalle.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0D4A6B')),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 9),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
                ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
                ('FONTSIZE', (0,1), (-1,-1), 8),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E0E0E0')),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8F9FA')]),
                ('TOPPADDING', (0,0), (-1,-1), 5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ]))
            elements.append(t_detalle)
            if omitidos:
                elements.append(Spacer(1, 0.1*inch))
                elements.append(Paragraph(
                    f"<i>Nota: Se muestran 12 de {len(df)} periodos. La tabla completa está disponible en la app web.</i>",
                    description_style
                ))

        elements.append(PageBreak())

    # ======== MÓDULO B: JUBILACIÓN (similar mejoras) ========
    if datos_jubilacion:
        elements.append(Paragraph("💰 MÓDULO 2: PLANIFICACIÓN DE JUBILACIÓN", section_style))
        
        elements.append(Paragraph(
            "Este módulo calcula tu capacidad de retiro considerando impuestos y estructura de pagos. "
            "La sostenibilidad de tu jubilación depende de la relación entre tu capital neto, "
            "la inflación futura y tu esperanza de vida post-jubilación.",
            description_style
        ))

        # Tabla resumen
        impuesto_pct = (datos_jubilacion['impuesto'] / datos_jubilacion['ganancia'] * 100) if datos_jubilacion['ganancia'] > 0 else 0
        resumen_jub = [
            ['Concepto', 'Monto'],
            ['Capital Bruto', f"${datos_jubilacion['capital_bruto']:,.2f}"],
            ['Impuesto (29.5%)', f"${datos_jubilacion['impuesto']:,.2f}"],
            ['<b>Capital Neto</b>', f"<b>${datos_jubilacion['capital_neto']:,.2f}</b>"],
            ['Modalidad', datos_jubilacion['opcion_retiro']],
        ]
        if datos_jubilacion['opcion_retiro'] == 'Pensión Mensual':
            resumen_jub.extend([
                ['Plazo de Retiro', f"{datos_jubilacion['anos_retiro']} años"],
                ['Pensión Mensual', f"${datos_jubilacion['pension_mensual']:,.2f}"],
                ['Total Recibido', f"${datos_jubilacion['pension_mensual']*12*datos_jubilacion['anos_retiro']:,.2f}"],
            ])

        t_jub = Table(resumen_jub, colWidths=[3*inch, 2.8*inch])
        t_jub.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#FFF8E1')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#5D4037')),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 10),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#FFECB3')),
            ('BACKGROUND', (0,-3), (-1,-1), colors.HexColor('#FFECB3')) if 'Pensión' in datos_jubilacion.get('opcion_retiro','') else (),
            ('FONTNAME', (0,-3), (-1,-1), 'Helvetica-Bold') if 'Pensión' in datos_jubilacion.get('opcion_retiro','') else (),
        ]))
        elements.append(t_jub)
        elements.append(Spacer(1, 0.2*inch))

        # Insight
        if datos_jubilacion['opcion_retiro'] == 'Pensión Mensual':
            ratio = datos_jubilacion['pension_mensual'] / (datos_jubilacion['capital_neto'] / 12 / datos_jubilacion['anos_retiro']) if datos_jubilacion['capital_neto'] > 0 else 0
            if ratio < 0.04:
                insight = "<b>💡 Recomendación:</b> Tu tasa de retiro (4% anual) está dentro del rango seguro (3–4%)."
            else:
                insight = "<b>⚠️ Alerta:</b> Tu tasa de retiro supera el 4% anual. Considera extender el plazo o reducir la pensión."
        else:
            insight = "<b>🔍 Consideración:</b> El retiro total expone tu capital a riesgo de mercado posterior. Una pensión escalonada puede ser más eficiente fiscalmente."
        elements.append(Paragraph(insight, insight_style))
        elements.append(Spacer(1, 0.2*inch))

        if 'grafico' in datos_jubilacion and datos_jubilacion['grafico']:
            try:
                img = Image(io.BytesIO(datos_jubilacion['grafico']), width=6.2*inch, height=2.8*inch)
                elements.append(Paragraph("Estructura de Retiro Proyectado", description_style))
                elements.append(img)
            except:
                pass
        elements.append(PageBreak())

    # ======== MÓDULO C: BONOS (con flujos detallados) ========
    if datos_bono:
        elements.append(Paragraph("📉 MÓDULO 3: VALORACIÓN DE BONOS", section_style))
        
        elements.append(Paragraph(
            "La valoración de bonos se basa en el <b>Valor Presente de Flujos de Caja</b> (DCF), descontando "
            "los cupones y valor nominal a la tasa de mercado. Un bono es atractivo cuando su VP > valor nominal.",
            description_style
        ))

        diff = datos_bono['vp_total'] - datos_bono['valor_nominal']
        diff_pct = diff / datos_bono['valor_nominal'] * 100
        estado = "SUBVALUADO 🟢" if diff < 0 else "SOBREVALUADO 🔴" if diff > 0 else "A LA PAR ⚪"

        resumen_bono = [
            ['Parámetro', 'Valor'],
            ['Valor Nominal', f"${datos_bono['valor_nominal']:,.2f}"],
            ['Tasa Cupón', f"{datos_bono['tasa_cupon']:.2f}% anual"],
            ['Plazo', f"{datos_bono['anos']} años"],
            ['TEA de Mercado', f"{datos_bono['tea_mercado']:.2f}%"],
            ['Valor Presente', f"${datos_bono['vp_total']:,.2f}"],
            ['Diferencia', f"{diff:+,.2f} ({diff_pct:+.2f}%)"],
            ['<b>Recomendación</b>', f"<b>{estado}</b>"],
        ]

        t_bono = Table(resumen_bono, colWidths=[3*inch, 2.8*inch])
        t_bono.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F3E5F5')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#4A148C')),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 10),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CE93D8')),
            ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#CE93D8')),
            ('TEXTCOLOR', (0,-1), (-1,-1), colors.white),
            ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ]))
        elements.append(t_bono)
        elements.append(Spacer(1, 0.2*inch))

        # Insight
        if diff_pct < -5:
            insight = "<b>🟢 Oportunidad:</b> El bono está subvaluado >5%. Podría generar ganancia de capital al vencimiento."
        elif diff_pct > 5:
            insight = "<b>🔴 Riesgo:</b> Prima de precio >5%. Solo justificable si buscas ingreso fijo y mantendrás hasta vencimiento."
        else:
            insight = "<b>⚪ Neutral:</b> Precio cercano a par. Evalúa según tu apetito por duración y flujo de caja."
        elements.append(Paragraph(insight, insight_style))
        elements.append(Spacer(1, 0.2*inch))

        # Gráfico
        if 'grafico' in datos_bono and datos_bono['grafico']:
            try:
                img = Image(io.BytesIO(datos_bono['grafico']), width=6.2*inch, height=2.8*inch)
                elements.append(Paragraph("Flujos de Caja Descontados", description_style))
                elements.append(img)
                elements.append(Spacer(1, 0.2*inch))
            except:
                pass

        # Tabla detallada de flujos → ✅ AHORA SÍ SE MUESTRA
        if 'df' in datos_bono and isinstance(datos_bono['df'], pd.DataFrame) and not datos_bono['df'].empty:
            elements.append(Paragraph("Flujos de Caja Detallados (Cupones + Valor Nominal)", description_style))
            
            df = datos_bono['df']
            if len(df) > 12:
                df_show = pd.concat([df.head(6), df.tail(6)])
                omitidos = len(df) - 12
            else:
                df_show = df
                omitidos = 0
            
            data = [['Periodo', 'Flujo', 'Factor Desc.', 'VP del Flujo']]
            for _, r in df_show.iterrows():
                data.append([
                    str(int(r['Periodo'])),
                    f"${r['Flujo']:,.2f}",
                    f"{r['Factor']:.4f}",
                    f"${r['VP Flujo']:,.2f}"
                ])
            
            if omitidos > 0:
                data.insert(7, ['…', '…', '…', '…'])
            
            t_flujos = Table(data, colWidths=[1*inch, 1.6*inch, 1.6*inch, 2.6*inch])
            t_flujos.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#4A148C')),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 9),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
                ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
                ('FONTSIZE', (0,1), (-1,-1), 8),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E1BEE7')),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F3E5F5')]),
            ]))
            elements.append(t_flujos)

            vp_total_calc = df['VP Flujo'].sum()
            elements.append(Spacer(1, 0.1*inch))
            elements.append(Paragraph(
                f"<i>Suma de VP de flujos: <b>${vp_total_calc:,.2f}</b> | Diferencia vs reportado: {abs(vp_total_calc - datos_bono['vp_total']):.2f}</i>",
                description_style
            ))

    # ======== NOTA FINAL ========
    elements.append(Spacer(1, 0.5*inch))
    footer_style = ParagraphStyle(
        'Footer',
        fontSize=8,
        textColor=colors.HexColor('#6B7280'),
        alignment=TA_CENTER,
        fontName='Helvetica-Oblique'
    )
    elements.append(Paragraph(
        "⚠️ <i>Este reporte es informativo y no constituye asesoría financiera, fiscal o legal. "
        "Las proyecciones asumen estabilidad en tasas, inflación y marco regulatorio. "
        "Recomendamos validar con un asesor certificado antes de tomar decisiones.</i>",
        footer_style
    ))

    # Generar PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer
