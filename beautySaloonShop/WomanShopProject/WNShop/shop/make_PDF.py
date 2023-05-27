from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

def create_pdf(user, items, order_date, total_cost):
    doc = SimpleDocTemplate(f"orders/{user}_order_{order_date}.pdf", pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    styles['Normal'].fontName='DejaVuSerif'
    styles['Heading1'].fontName='DejaVuSerif'
    pdfmetrics.registerFont(TTFont('DejaVuSerif','DejaVuSerif.ttf', 'UTF-8'))

    # Заголовок
    title = Paragraph("<h1>Заказ</h1>", styles["Heading1"])
    elements.append(title)

    table = Table(
    [
        [Paragraph('Пользователь', styles["Normal"]), Paragraph('Дата заказа', styles["Normal"]), Paragraph('Товары', styles["Normal"]), Paragraph('Общая стоимость', styles["Normal"])],
        [Paragraph(f'{user}', styles["Normal"]), Paragraph(f'{order_date}', styles["Normal"]), Paragraph(', '.join(items), styles["Normal"]), Paragraph(f'{total_cost}', styles["Normal"])]
    ]
    )
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    elements.append(table)

    # Создание документа
    doc.build(elements)


