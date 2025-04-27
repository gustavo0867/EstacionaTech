from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf_report(data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []

    # Cabeçalho
    elements.append(Paragraph(f"<b>EstacionaTech - Relatório de Faturamento</b>", styles['Title']))
    elements.append(Paragraph(f"Período: {data['periodo']}", styles['Normal']))

    # Dados da tabela
    table_data = [
        ["Data/Hora", "Valor", "Forma Pagamento", "Placa", "Cliente"]
    ]

    for item in data['dados']:
        table_data.append([
            item['data'],
            f"R$ {item['valor']:.2f}",
            item['forma_pagamento'],
            item['placa'],
            item['cliente']
        ])

    # Criar tabela
    t = Table(table_data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(t)
    elements.append(Paragraph(f"<b>Total Arrecadado: R$ {data['total']:.2f}</b>", styles['Normal']))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()