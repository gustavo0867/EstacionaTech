from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
import io

styles = getSampleStyleSheet()
styles['Heading3'].alignment = TA_CENTER #Define o h3 como centralizado, será usado apenas para subtitulos
def criar_PDF(locacoes):

    buffer = io.BytesIO()
    cnv = canvas.Canvas(buffer, pagesize=A4)
    cnv.drawString(100, 800, "Relatorio Operacional")

    #for id_locacao in dados_locacoes:

def relatorio_locacoes(locacoes: list, data_inicio, data_fim):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=35, rightMargin=40, topMargin=40, bottomMargin=40)
    elementos = []

    adicionar_logo(elementos)

    adicionar_titulo(elementos, "Relatório de Locações")

    adicionar_subtitulo(elementos, data_inicio, data_fim)

    # Cabeçalho da tabela
    dados_tabela = [
        ['ID Locação', 'ID Vaga', 'Placa Veículo', 'Id Operador', 'Entrada', 'Saída']
    ]

    # Preenche as linhas com os dados das locações
    for loc in locacoes:
        dados_tabela.append([
            str(loc[0]),  # id_locacao
            str(loc[1]),  # id_vaga
            str(loc[2]),  # id_veiculo
            str(loc[3]),  # id_operador
            str(loc[4]),  #data_hora_entrada
            str(loc[5]),  # data_hora_saida
        ])

    # Criação da tabela
    tabela = Table(dados_tabela, repeatRows=1, colWidths=[2 * cm, 2 * cm, 2.5 * cm, 4 * cm, 5 * cm, 5 * cm])
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))

    elementos.append(tabela)
    doc.build(elementos)

    buffer.seek(0)
    return buffer

def relatorio_operacional(vagas, tempo_medio, data_inicio, data_fim):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=35, rightMargin=40, topMargin=40, bottomMargin=40)
    elementos = []

    adicionar_logo(elementos)

    adicionar_titulo(elementos, "Relatório Operacional Geral")

    adicionar_subtitulo(elementos, data_inicio, data_fim)

    titulo_vagas = Paragraph("Vagas Mais Utilizadas: ", styles['Heading4'])
    elementos.append(titulo_vagas)

    # Cabeçalho da tabela
    dados_tabela = [
        ['ID Vaga', 'Qtde. de Utilização']
    ]

    for vaga in vagas:
        dados_tabela.append([
            str(vaga[0]),
            str(vaga[1]) #qtde de uso
        ])

    tabela = Table(dados_tabela, repeatRows=1, colWidths=[3 * cm, 3 * cm])
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))

    elementos.append(tabela)

    titulo_tempo_medio = Paragraph("Tempo Médio de Permanência no Estacionamento: ", styles['Heading4'])
    elementos.append(titulo_tempo_medio)
    info_tempo_medio = Paragraph(str(tempo_medio))
    elementos.append(info_tempo_medio)

    doc.build(elementos)

    buffer.seek(0)
    return buffer

def relatorio_financeiro(faturamento_total, faturamento_por_dia, media_diaria, data_inicio, data_fim):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=35, rightMargin=40, topMargin=40, bottomMargin=40)
    elementos = []

    adicionar_logo(elementos)

    adicionar_titulo(elementos, "Relatório Financeiro Geral")

    adicionar_subtitulo(elementos, data_inicio, data_fim)

    titulo_faturamento_total = Paragraph("Faturamento Total: ", styles['Heading4'])
    elementos.append(titulo_faturamento_total)
    info_faturamento_total = Paragraph(f"R$: {str(faturamento_total)}")
    elementos.append(info_faturamento_total)

    titulo_faturamento_por_dia = Paragraph("Faturamento Diário: ", styles['Heading4'])
    elementos.append(titulo_faturamento_por_dia)
    # Cabeçalho da tabela
    dados_tabela = [
        ['Data', 'Valor']
    ]

    for dia in faturamento_por_dia:
        dados_tabela.append([
            str(dia[0]),
            str(dia[1])  # qtde de uso
        ])

    tabela = Table(dados_tabela, repeatRows=1, colWidths=[3 * cm, 3 * cm])
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))

    elementos.append(tabela)

    titulo_media_diaria = Paragraph("Média de Faturamento Diária: ", styles['Heading4'])
    elementos.append(titulo_media_diaria)
    info_media_diaria = Paragraph(f"R$: {str(media_diaria)}")
    elementos.append(info_media_diaria)

    doc.build(elementos)

    buffer.seek(0)
    return buffer


def adicionar_logo(elementos):
    caminho_logo = "EstacionaTech/static/img/EstacionaTechLogo.jpeg"
    imagem_logo = Image(caminho_logo, width=110, height=50)
    imagem_logo.hAlign = 'LEFT'
    elementos.append(imagem_logo)
    elementos.append(Spacer(1, 10))

def adicionar_titulo(elementos, tipo_relatorio):
    # Título
    titulo = Paragraph(tipo_relatorio, styles['Title'])
    elementos.append(titulo)
    elementos.append(Spacer(1, 0.5 * cm))
def adicionar_subtitulo(elementos, data_inicio, data_fim):
    subtitulo = Paragraph(f"Intervalo observado: {data_inicio} a {data_fim}", styles['Heading3'])
    elementos.append(subtitulo)
    elementos.append(Spacer(1, 0.5 * cm))