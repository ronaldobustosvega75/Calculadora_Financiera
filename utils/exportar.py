from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from datetime import datetime
import io
from reportlab.platypus import Image

def generar_pdf_reporte(datos_cartera, datos_jubilacion, datos_bono=None):
    """Genera un PDF con el reporte completo en estilo profesional"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=10,
        alignment=1,
        fontName='Helvetica-Bold'
    )
    
    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#34495E'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold',
        borderWidth=0,
        borderColor=colors.HexColor('#BDC3C7'),
        borderPadding=5
    )
    
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#7F8C8D'),
        alignment=1
    )
    
    elements.append(Paragraph("REPORTE FINANCIERO", title_style))
    elements.append(Paragraph(f"Generado el {datetime.now().strftime('%d/%m/%Y')}", date_style))
    elements.append(Spacer(1, 0.4*inch))
    
    if datos_cartera:
        elements.append(Paragraph("Proyección de Cartera", section_style))
        elements.append(Spacer(1, 0.15*inch))
        
        info = [
            ['Descripción', 'Valor'],
            ['Monto Inicial', f"$ {datos_cartera['monto_inicial']:,.2f}"],
            ['Aporte Periódico', f"$ {datos_cartera['aporte_periodico']:,.2f}"],
            ['Tasa Efectiva Anual (TEA)', f"{datos_cartera['tea']:.2f}%"],
            ['Plazo', f"{datos_cartera['anos']} años"],
            ['Saldo Final Proyectado', f"$ {datos_cartera['saldo_final']:,.2f}"],
        ]
        
        t = Table(info, colWidths=[3.5*inch, 2.5*inch])
        t.setStyle(TableStyle([
            
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8E8E8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
            ('LINEABOVE', (0, 0), (-1, 0), 1.5, colors.HexColor('#7F8C8D')),
            ('LINEBELOW', (0, -1), (-1, -1), 1.5, colors.HexColor('#7F8C8D')),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#F8F9FA')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.35*inch))
        
        if 'grafico' in datos_cartera:
            img = io.BytesIO(datos_cartera['grafico'])
            elements.append(Image(img, width=5.5*inch, height=3*inch))
            elements.append(Spacer(1, 0.25*inch))
    
    
    if datos_jubilacion:
        elements.append(Paragraph("Proyección de Jubilación", section_style))
        elements.append(Spacer(1, 0.15*inch))
        
        info = [
            ['Descripción', 'Valor'],
            ['Capital Acumulado (Bruto)', f"$ {datos_jubilacion['capital_bruto']:,.2f}"],
            ['Ganancia Generada', f"$ {datos_jubilacion['ganancia']:,.2f}"],
            ['Impuesto a la Renta', f"$ {datos_jubilacion['impuesto']:,.2f}"],
            ['Capital Neto Disponible', f"$ {datos_jubilacion['capital_neto']:,.2f}"],
            ['Pensión Mensual Estimada', f"$ {datos_jubilacion['pension_mensual']:,.2f}"],
        ]
        
        t = Table(info, colWidths=[3.5*inch, 2.5*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8E8E8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
            ('LINEABOVE', (0, 0), (-1, 0), 1.5, colors.HexColor('#7F8C8D')),
            ('LINEBELOW', (0, -1), (-1, -1), 1.5, colors.HexColor('#7F8C8D')),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#F8F9FA')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.35*inch))
        
        if 'grafico' in datos_jubilacion:
            img = io.BytesIO(datos_jubilacion['grafico'])
            elements.append(Image(img, width=5.5*inch, height=3*inch))
            elements.append(Spacer(1, 0.25*inch))
    
    if datos_bono:
        elements.append(Paragraph("Valoración de Bono", section_style))
        elements.append(Spacer(1, 0.15*inch))
        
        
        
        info = [
            ['Descripción', 'Valor'],
            ['Valor Nominal', f"$ {datos_bono['valor_nominal']:,.2f}"],
            ['Tasa de Cupón', f"{datos_bono['tasa_cupon']:.2f}%"],
            ['Plazo del Bono', f"{datos_bono['anos']} años"],
            ['Valor Presente Total', f"$ {datos_bono['vp_total']:,.2f}"],
        ]
        
        t = Table(info, colWidths=[3.5*inch, 2.5*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8E8E8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
            ('LINEABOVE', (0, 0), (-1, 0), 1.5, colors.HexColor('#7F8C8D')),
            ('LINEBELOW', (0, -1), (-1, -1), 1.5, colors.HexColor('#7F8C8D')),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#F8F9FA')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.15*inch))
        if 'grafico' in datos_bono:
            img = io.BytesIO(datos_bono['grafico'])
            elements.append(Image(img, width=5.5*inch, height=3*inch))
            elements.append(Spacer(1, 0.25*inch))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer