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
    #doc.build(elementos)
    doc.build(elementos, onFirstPage=rodape, onLaterPages=rodape)


    buffer.seek(0)
    return buffer

def relatorio_operacional_geral(vagas, tempo_medio, maior_movimento, menor_movimento, data_inicio, data_fim):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=35, rightMargin=40, topMargin=40, bottomMargin=40)
    elementos = []

    adicionar_logo(elementos)

    adicionar_titulo(elementos, "Relatório Operacional Geral")

    adicionar_subtitulo(elementos, data_inicio, data_fim)

    titulo_vagas = Paragraph("Vagas Mais Utilizadas: ", styles['Heading4'])
    elementos.append(titulo_vagas)

    # Cabeçalho da tabela
    dados_tabela_vagas = [
        ['ID Vaga', 'Qtde. de Utilização']
    ]

    for vaga in vagas:
        dados_tabela_vagas.append([
            str(vaga[0]),
            str(vaga[1]) #qtde de uso
        ])

    tabela_vagas = Table(dados_tabela_vagas, repeatRows=1, colWidths=[3 * cm, 3 * cm])
    tabela_vagas.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))

    elementos.append(tabela_vagas)

    # *** TEMPO MEDIO DE PERMANENCIA ***
    elementos.append(Spacer(1, 0.5 * cm))
    titulo_tempo_medio = Paragraph("Tempo Médio de Permanência no Estacionamento: ", styles['Heading4'])
    elementos.append(titulo_tempo_medio)
    info_tempo_medio = Paragraph(str(tempo_medio))
    elementos.append(info_tempo_medio)

    # ** MOVIMENTO NAS FAIXAS DE HORÁRIO
    elementos.append(Spacer(1, 0.5 * cm))
    titulo_movimento_horarios = Paragraph("Movimento nas Faixas de Horário: ", styles['Heading4'])
    elementos.append(titulo_movimento_horarios)

    # Cabeçalho da tabela de HORÁRIOS
    dados_tabela_horarios = [
        ['Faixa de Horário c/ MAIOR Movimento', 'Faixa de Horário c/ MENOR Movimento']
    ]#como add chave ssh do ubuntu wsl no github


    dados_tabela_horarios.append([
        maior_movimento,
        menor_movimento
    ])

    tabela_horarios = Table(dados_tabela_horarios, repeatRows=1, colWidths=[6 * cm, 6 * cm])
    tabela_horarios.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))

    elementos.append(tabela_horarios)



    doc.build(elementos, onFirstPage=rodape, onLaterPages=rodape)

    buffer.seek(0)
    return buffer

def relatorio_operacional_clientes(mensalistas, clientes_mais_veiculos, clientes_frequentes):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=35, rightMargin=40, topMargin=40, bottomMargin=40)
    elementos = []

    adicionar_logo(elementos)

    adicionar_titulo(elementos, "Relatório Operacional de Clientes")

    titulo_mensalistas = Paragraph("Mensalistas Ativos: ", styles['Heading4'])
    elementos.append(titulo_mensalistas)

    # Cabeçalho da tabela
    dados_tabela_mensalistas = [
        ['ID Mensalista', 'CPF', 'Nome', 'Telefone', 'Email', 'Modalidade']
    ]

    for mensalista in mensalistas:
        dados_tabela_mensalistas.append([
            str(mensalista[0]),
            str(mensalista[1]),
            str(mensalista[2]),
            str(mensalista[3]),
            str(mensalista[4]),
            str(mensalista[5])
        ])

    tabela_mensalistas = Table(dados_tabela_mensalistas, repeatRows=1, colWidths=[3 * cm, 3 * cm, 4 * cm, 3 * cm, 4 * cm, 3 * cm])
    tabela_mensalistas.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))

    elementos.append(tabela_mensalistas)

    # *** CLIENTES COM MAIS VEICULOS ***
    elementos.append(Spacer(1, 0.5 * cm))
    titulo_clientes_mais_veiculos = Paragraph("Clientes Com Mais Veículos: ", styles['Heading4'])
    elementos.append(titulo_clientes_mais_veiculos)

    # Cabeçalho da tabela
    dados_tabela_clientes_mais_veiculos = [
        ['ID Mensalista', 'CPF', 'Nome', 'Telefone', 'Email', 'Mensalista','Modalidade', 'Qtde.']
    ]

    for cliente in clientes_mais_veiculos:
        if cliente[5] == 1:
            is_mensalista = 'Sim'
        else:
            is_mensalista = 'Não'
        dados_tabela_clientes_mais_veiculos.append([
            str(cliente[0]),
            str(cliente[1]),
            str(cliente[2]),
            str(cliente[3]),
            str(cliente[4]),
            is_mensalista,
            str(cliente[6]),
            str(cliente[7])
        ])

    tabela_clientes_mais_veiculos = Table(dados_tabela_clientes_mais_veiculos, repeatRows=1,
                               colWidths=[2.5 * cm, 2.5 * cm, 3 * cm, 2.5 * cm, 4 * cm, 2 * cm, 2.5 * cm, 1.5 * cm])
    tabela_clientes_mais_veiculos.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))

    elementos.append(tabela_clientes_mais_veiculos)

    # ***** CLIENTES FREQUENTES ******
    elementos.append(Spacer(1, 0.5 * cm))
    titulo_clientes_frequentes = Paragraph("Clientes Frequentes: ", styles['Heading4'])
    elementos.append(titulo_clientes_frequentes)

    # Cabeçalho da tabela
    dados_tabela_clientes_frequentes = [
        ['ID Mensalista', 'CPF', 'Nome', 'Telefone', 'Email', 'Mensalista', 'Modalidade', 'Nº Locações']
    ]

    for cliente in clientes_frequentes:
        if cliente[5] == 1:
            is_mensalista = 'Sim'
        else:
            is_mensalista = 'Não'
        dados_tabela_clientes_frequentes.append([
            str(cliente[0]),
            str(cliente[1]),
            str(cliente[2]),
            str(cliente[3]),
            str(cliente[4]),
            is_mensalista,
            str(cliente[6]),
            str(cliente[7])
        ])

    tabela_clientes_frequentes = Table(dados_tabela_clientes_frequentes, repeatRows=1,
                                          colWidths=[2.5 * cm, 2.5 * cm, 3 * cm, 2.5 * cm, 4 * cm, 2 * cm, 2 * cm,
                                                     2 * cm])
    tabela_clientes_frequentes.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))

    elementos.append(tabela_clientes_frequentes)

    doc.build(elementos, onFirstPage=rodape, onLaterPages=rodape)

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

    doc.build(elementos, onFirstPage=rodape, onLaterPages=rodape)

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

def rodape(canvas: canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica-Oblique', 10)
    canvas.drawCentredString(A4[0] / 2, 15, "Relatório Emitido Via EstacionaTech")
    canvas.restoreState()
