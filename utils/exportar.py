from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle, Paragraph, 
                                Spacer, PageBreak, Image, KeepTogether)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
import io
import pandas as pd


def generar_pdf_reporte(datos_cartera, datos_jubilacion, datos_bono=None):
    """Genera un PDF con el reporte completo en estilo profesional"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=40,
        bottomMargin=40
    )
    elements = []
    styles = getSampleStyleSheet()
    
    # ============== ESTILOS PERSONALIZADOS ==============
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1A5490'),
        spaceAfter=8,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#5D6D7E'),
        alignment=TA_CENTER,
        spaceAfter=20
    )
    
    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.white,
        spaceAfter=15,
        spaceBefore=25,
        fontName='Helvetica-Bold',
        backColor=colors.HexColor('#1A5490'),
        borderPadding=8,
        alignment=TA_LEFT
    )
    
    subsection_style = ParagraphStyle(
        'SubsectionTitle',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )
    
    description_style = ParagraphStyle(
        'Description',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#34495E'),
        alignment=TA_JUSTIFY,
        spaceAfter=10
    )
    
    # ============== ENCABEZADO DEL REPORTE ==============
    elements.append(Paragraph("REPORTE DE PROYECCIÓN FINANCIERA", title_style))
    elements.append(Paragraph(
        f"Análisis Integral de Inversión y Jubilación<br/>"
        f"Generado el {datetime.now().strftime('%d de %B del %Y a las %H:%M')}", 
        subtitle_style
    ))
    elements.append(Spacer(1, 0.3*inch))
    
    # Línea separadora
    line = Table([['']], colWidths=[7*inch])
    line.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#1A5490')),
    ]))
    elements.append(line)
    elements.append(Spacer(1, 0.2*inch))
    
    # ============== MÓDULO A: PROYECCIÓN DE CARTERA ==============
    if datos_cartera:
        elements.append(Paragraph("📊 MÓDULO A: CRECIMIENTO DE CARTERA", section_style))
        elements.append(Spacer(1, 0.15*inch))
        
        # Descripción
        desc = (
            f"Esta proyección muestra cómo tu inversión inicial de "
            f"<b>${datos_cartera['monto_inicial']:,.2f}</b> crecerá durante "
            f"<b>{datos_cartera['anos']} años</b> con aportes {datos_cartera.get('frecuencia', 'periódicos').lower()}s de "
            f"<b>${datos_cartera['aporte_periodico']:,.2f}</b> y una tasa efectiva anual (TEA) del "
            f"<b>{datos_cartera['tea']:.2f}%</b>."
        )
        elements.append(Paragraph(desc, description_style))
        elements.append(Spacer(1, 0.15*inch))
        
        # Tabla de resumen
        ganancia = datos_cartera['saldo_final'] - datos_cartera['total_aportes']
        rentabilidad = (ganancia / datos_cartera['total_aportes'] * 100) if datos_cartera['total_aportes'] > 0 else 0
        
        info = [
            ['Concepto', 'Monto', 'Detalle'],
            ['Monto Inicial', f"${datos_cartera['monto_inicial']:,.2f}", 'Capital de inicio'],
            ['Aporte Periódico', f"${datos_cartera['aporte_periodico']:,.2f}", f"Frecuencia: {datos_cartera.get('frecuencia', 'Mensual')}"],
            ['TEA Aplicada', f"{datos_cartera['tea']:.2f}%", 'Tasa efectiva anual'],
            ['Plazo de Inversión', f"{datos_cartera['anos']} años", f"{datos_cartera['anos'] * 12} meses"],
            ['Total Aportado', f"${datos_cartera['total_aportes']:,.2f}", 'Capital + aportes acumulados'],
            ['Ganancia por Intereses', f"${ganancia:,.2f}", f"Rentabilidad: {rentabilidad:.1f}%"],
            ['SALDO FINAL', f"${datos_cartera['saldo_final']:,.2f}", 'Capital total proyectado'],
        ]
        
        t = Table(info, colWidths=[2.3*inch, 1.8*inch, 2.7*inch])
        t.setStyle(TableStyle([
            # Encabezado
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495E')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            # Contenido
            ('BACKGROUND', (0, 1), (-1, -2), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -2), colors.HexColor('#2C3E50')),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
            ('ALIGN', (2, 1), (2, -1), 'LEFT'),
            ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -2), 9),
            # Fila final destacada
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#D5F4E6')),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.HexColor('#0E6655')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 11),
            # Bordes y padding
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
            ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#1A5490')),
            ('LINEBELOW', (0, -1), (-1, -1), 2, colors.HexColor('#0E6655')),
            # Alternar colores de fila
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#F8F9FA')]),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.25*inch))
        
        # Gráfico si está disponible
        if 'grafico' in datos_cartera and datos_cartera['grafico'] is not None:
            elements.append(Paragraph("Evolución de la Inversión", subsection_style))
            try:
                img = io.BytesIO(datos_cartera['grafico'])
                elements.append(Image(img, width=6*inch, height=3.3*inch))
            except:
                elements.append(Paragraph("<i>Gráfico no disponible</i>", description_style))
            elements.append(Spacer(1, 0.2*inch))
        
        # Tabla detallada (primeras 5 y últimas 5 filas)
        if 'df' in datos_cartera and datos_cartera['df'] is not None:
            elements.append(Paragraph("Detalle de Periodos (Primeros y Últimos 5)", subsection_style))
            
            df = datos_cartera['df']
            if len(df) > 10:
                df_mostrar = pd.concat([df.head(5), df.tail(5)])
                elementos_omitidos = len(df) - 10
            else:
                df_mostrar = df
                elementos_omitidos = 0
            
            # Preparar datos para la tabla
            tabla_data = [['Periodo', 'Aporte', 'Interés', 'Saldo']]
            for _, row in df_mostrar.iterrows():
                tabla_data.append([
                    f"{int(row['Periodo'])}",
                    f"${row['Aporte']:,.0f}",
                    f"${row['Interes']:,.0f}",
                    f"${row['Saldo']:,.0f}"
                ])
            
            # Agregar fila de puntos suspensivos si hay elementos omitidos
            if elementos_omitidos > 0:
                pos_insert = 6  # Después de las primeras 5 + encabezado
                tabla_data.insert(pos_insert, ['...', '...', '...', '...'])
            
            t_detalle = Table(tabla_data, colWidths=[1*inch, 1.6*inch, 1.6*inch, 1.8*inch])
            t_detalle.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#5DADE2')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#EBF5FB')]),
            ]))
            elements.append(t_detalle)
            
            if elementos_omitidos > 0:
                elements.append(Spacer(1, 0.1*inch))
                elements.append(Paragraph(
                    f"<i>Se omitieron {elementos_omitidos} periodos intermedios para mantener el reporte conciso.</i>",
                    description_style
                ))
        
        elements.append(PageBreak())
    
    # ============== MÓDULO B: PROYECCIÓN DE JUBILACIÓN ==============
    if datos_jubilacion:
        elements.append(Paragraph("💰 MÓDULO B: PROYECCIÓN DE JUBILACIÓN", section_style))
        elements.append(Spacer(1, 0.15*inch))
        
        # Descripción
        tipo_impuesto_texto = "fuente extranjera (29.5%)" if datos_jubilacion.get('tipo_impuesto') == 'extranjera' else "bolsa local (5%)"
        desc = (
            f"Este análisis calcula tu pensión mensual considerando un capital acumulado de "
            f"<b>${datos_jubilacion['capital_bruto']:,.2f}</b>, aplicando impuestos por inversión de {tipo_impuesto_texto}. "
        )
        if datos_jubilacion.get('opcion_retiro') == 'Pensión Mensual':
            desc += (
                f"Recibirás una pensión mensual de <b>${datos_jubilacion['pension_mensual']:,.2f}</b> "
                f"durante <b>{datos_jubilacion.get('anos_retiro', 'N/A')} años</b>."
            )
        else:
            desc += "Optaste por un <b>cobro total</b> en un solo pago."
        
        elements.append(Paragraph(desc, description_style))
        elements.append(Spacer(1, 0.15*inch))
        
        # Tabla de resumen
        tasa_impuesto = (datos_jubilacion['impuesto'] / datos_jubilacion['ganancia'] * 100) if datos_jubilacion['ganancia'] > 0 else 0
        
        info = [
            ['Concepto', 'Monto', 'Detalle'],
            ['Capital Bruto', f"${datos_jubilacion['capital_bruto']:,.2f}", 'Saldo total antes de impuestos'],
            ['Total Aportado', f"${datos_jubilacion['total_aportes']:,.2f}", 'Suma de tus inversiones'],
            ['Ganancia Generada', f"${datos_jubilacion['ganancia']:,.2f}", 'Rendimiento de tu inversión'],
            ['Impuesto a la Renta', f"${datos_jubilacion['impuesto']:,.2f}", f"Tasa: {tasa_impuesto:.2f}% sobre ganancia"],
            ['CAPITAL NETO', f"${datos_jubilacion['capital_neto']:,.2f}", 'Disponible para retiro'],
        ]
        
        if datos_jubilacion.get('opcion_retiro') == 'Pensión Mensual':
            info.append(['Pensión Mensual', f"${datos_jubilacion['pension_mensual']:,.2f}", 
                        f"Durante {datos_jubilacion.get('anos_retiro', 'N/A')} años"])
            info.append(['Total a Recibir', f"${datos_jubilacion['pension_mensual'] * datos_jubilacion.get('anos_retiro', 0) * 12:,.2f}", 
                        f"{datos_jubilacion.get('anos_retiro', 0) * 12} pagos mensuales"])
        
        t = Table(info, colWidths=[2.3*inch, 1.8*inch, 2.7*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495E')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#2C3E50')),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
            ('ALIGN', (2, 1), (2, -1), 'LEFT'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BACKGROUND', (0, -2), (-1, -1), colors.HexColor('#FCF3CF')),
            ('FONTNAME', (0, -2), (-1, -1), 'Helvetica-Bold'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
            ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#1A5490')),
            ('LINEBELOW', (0, -1), (-1, -1), 2, colors.HexColor('#F39C12')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -3), [colors.white, colors.HexColor('#F8F9FA')]),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.25*inch))
        
        # Gráfico si está disponible
        if 'grafico' in datos_jubilacion and datos_jubilacion['grafico'] is not None:
            elements.append(Paragraph("Proyección de Retiro Mensual", subsection_style))
            try:
                img = io.BytesIO(datos_jubilacion['grafico'])
                elements.append(Image(img, width=6*inch, height=3.3*inch))
            except:
                elements.append(Paragraph("<i>Gráfico no disponible</i>", description_style))
            elements.append(Spacer(1, 0.2*inch))
        
        elements.append(PageBreak())
    
    # ============== MÓDULO C: VALORACIÓN DE BONOS ==============
    if datos_bono:
        elements.append(Paragraph("📈 MÓDULO C: VALORACIÓN DE BONOS", section_style))
        elements.append(Spacer(1, 0.15*inch))
        
        # Descripción
        diferencia = datos_bono['vp_total'] - datos_bono['valor_nominal']
        estado = "sobrevaluado" if diferencia > 0 else "subvaluado" if diferencia < 0 else "a la par"
        
        desc = (
            f"Este análisis valora un bono con valor nominal de <b>${datos_bono['valor_nominal']:,.2f}</b>, "
            f"tasa de cupón del <b>{datos_bono['tasa_cupon']:.2f}%</b> y plazo de <b>{datos_bono['anos']} años</b>. "
            f"El valor presente calculado es <b>${datos_bono['vp_total']:,.2f}</b>, lo que indica que el bono está "
            f"<b>{estado}</b> ({diferencia:+,.2f} respecto al valor nominal)."
        )
        elements.append(Paragraph(desc, description_style))
        elements.append(Spacer(1, 0.15*inch))
        
        # Tabla de resumen
        porcentaje_dif = (diferencia / datos_bono['valor_nominal'] * 100)
        
        info = [
            ['Concepto', 'Valor', 'Detalle'],
            ['Valor Nominal', f"${datos_bono['valor_nominal']:,.2f}", 'Valor facial del bono'],
            ['Tasa de Cupón', f"{datos_bono['tasa_cupon']:.2f}%", f"Frecuencia: {datos_bono.get('frecuencia_pago', 'Anual')}"],
            ['Plazo del Bono', f"{datos_bono['anos']} años", 'Tiempo hasta vencimiento'],
            ['TEA de Mercado', f"{datos_bono.get('tea_mercado', 'N/A')}%", 'Tasa de descuento aplicada'],
            ['VALOR PRESENTE', f"${datos_bono['vp_total']:,.2f}", f"Diferencia: {porcentaje_dif:+.2f}%"],
            ['Estado', estado.upper(), 'Interpretación del precio'],
        ]
        
        t = Table(info, colWidths=[2.3*inch, 1.8*inch, 2.7*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495E')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('BACKGROUND', (0, 1), (-1, -2), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -2), colors.HexColor('#2C3E50')),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
            ('ALIGN', (2, 1), (2, -1), 'LEFT'),
            ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -2), 9),
            ('BACKGROUND', (0, -2), (-1, -1), colors.HexColor('#E8DAEF')),
            ('FONTNAME', (0, -2), (-1, -1), 'Helvetica-Bold'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
            ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#1A5490')),
            ('LINEBELOW', (0, -1), (-1, -1), 2, colors.HexColor('#8E44AD')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -3), [colors.white, colors.HexColor('#F8F9FA')]),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.25*inch))
        
        # Gráfico si está disponible
        if 'grafico' in datos_bono and datos_bono['grafico'] is not None:
            elements.append(Paragraph("Flujos de Caja del Bono", subsection_style))
            try:
                img = io.BytesIO(datos_bono['grafico'])
                elements.append(Image(img, width=6*inch, height=3.3*inch))
            except:
                elements.append(Paragraph("<i>Gráfico no disponible</i>", description_style))
            elements.append(Spacer(1, 0.2*inch))
        
        # Tabla de flujos detallada
        if 'df' in datos_bono and datos_bono['df'] is not None:
            elements.append(Paragraph("Detalle de Flujos de Caja (Primeros y Últimos 5)", subsection_style))
            
            df = datos_bono['df']
            if len(df) > 10:
                df_mostrar = pd.concat([df.head(5), df.tail(5)])
                elementos_omitidos = len(df) - 10
            else:
                df_mostrar = df
                elementos_omitidos = 0
            
            tabla_data = [['Periodo', 'Flujo', 'Factor Desc.', 'VP Flujo']]
            for _, row in df_mostrar.iterrows():
                tabla_data.append([
                    f"{int(row['Periodo'])}",
                    f"${row['Flujo']:,.2f}",
                    f"{row.get('Factor', 0):.4f}" if 'Factor' in row else "N/A",
                    f"${row['VP Flujo']:,.2f}"
                ])
            
            if elementos_omitidos > 0:
                pos_insert = 6
                tabla_data.insert(pos_insert, ['...', '...', '...', '...'])
            
            t_detalle = Table(tabla_data, colWidths=[1*inch, 1.5*inch, 1.5*inch, 1.8*inch])
            t_detalle.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#A569BD')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F4ECF7')]),
            ]))
            elements.append(t_detalle)
            
            if elementos_omitidos > 0:
                elements.append(Spacer(1, 0.1*inch))
                elements.append(Paragraph(
                    f"<i>Se omitieron {elementos_omitidos} periodos intermedios. Valor presente total: ${datos_bono['vp_total']:,.2f}</i>",
                    description_style
                ))
    
    # ============== PIE DE PÁGINA ==============
    elements.append(Spacer(1, 0.5*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#95A5A6'),
        alignment=TA_CENTER
    )
    elements.append(Paragraph(
        "<i>Este reporte es generado automáticamente y tiene fines informativos. "
        "Las proyecciones están basadas en los parámetros ingresados y no constituyen asesoría financiera.</i>",
        footer_style
    ))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer
