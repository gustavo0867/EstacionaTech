from flask import Blueprint, render_template, request, send_file
from datetime import datetime
from io import BytesIO
import sys
from pathlib import Path

# Adiciona o caminho do projeto ao Python Path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Tenta importar de duas formas diferentes para garantir
try:
    from EstacionaTech.database.database import conectar
    from EstacionaTech.utils.pdf_generator import generate_pdf_report
except ImportError:
    from database.database import conectar
    from utils.pdf_generator import generate_pdf_report

relatorio_bp = Blueprint('relatorios', __name__, url_prefix='/relatorios')


@relatorio_bp.route('/')
def index():
    return render_template('relatorios.html')


@relatorio_bp.route('/gerar', methods=['POST'])
def gerar_relatorio():
    data_inicio = request.form.get('data_inicio')
    data_fim = request.form.get('data_fim', data_inicio)
    tipo = request.form.get('tipo_relatorio')

    conn = conectar()
    cursor = conn.cursor()

    # Consulta otimizada com tratamento de erro
    try:
        cursor.execute('''
            SELECT p.data_pagamento, p.valor, p.forma_pagamento, 
                   v.placa, c.nome as cliente_nome
            FROM Pagamento p
            JOIN Locacao l ON p.id_locacao = l.id_locacao
            JOIN Veiculo v ON l.id_veiculo = v.placa
            JOIN Cliente c ON v.id_cliente = c.id_cliente
            WHERE date(p.data_pagamento) BETWEEN ? AND ?
            ORDER BY p.data_pagamento DESC
        ''', (data_inicio, data_fim))

        pagamentos = cursor.fetchall()
        total = sum(p[1] for p in pagamentos)  # p[1] é o valor

        # Formata os dados para o template
        dados_formatados = [{
            'data': p[0].strftime('%d/%m/%Y %H:%M'),
            'valor': p[1],
            'forma_pagamento': p[2],
            'placa': p[3],
            'cliente': p[4]
        } for p in pagamentos]

    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")
        return render_template('error.html', message="Erro ao gerar relatório"), 500
    finally:
        conn.close()

    return render_template('relatorios_resultado.html',
                           pagamentos=dados_formatados,
                           total=total,
                           data_inicio=data_inicio,
                           data_fim=data_fim,
                           tipo=tipo)


@relatorio_bp.route('/exportar', methods=['POST'])
def exportar_pdf():
    data_inicio = request.form.get('data_inicio')
    data_fim = request.form.get('data_fim', data_inicio)

    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            SELECT p.data_pagamento, p.valor, p.forma_pagamento, 
                   v.placa, c.nome as cliente_nome
            FROM Pagamento p
            JOIN Locacao l ON p.id_locacao = l.id_locacao
            JOIN Veiculo v ON l.id_veiculo = v.placa
            JOIN Cliente c ON v.id_cliente = c.id_cliente
            WHERE date(p.data_pagamento) BETWEEN ? AND ?
            ORDER BY p.data_pagamento DESC
        ''', (data_inicio, data_fim))

        pagamentos = cursor.fetchall()
        total = sum(p[1] for p in pagamentos)

        # Prepara os dados para o PDF
        pdf_data = {
            'dados': [{
                'data': p[0].strftime('%d/%m/%Y %H:%M'),
                'valor': p[1],
                'forma_pagamento': p[2],
                'placa': p[3],
                'cliente': p[4]
            } for p in pagamentos],
            'total': total,
            'periodo': f"{datetime.strptime(data_inicio, '%Y-%m-%d').strftime('%d/%m/%Y')} a {datetime.strptime(data_fim, '%Y-%m-%d').strftime('%d/%m/%Y')}",
            'tipo': request.form.get('tipo_relatorio', 'diario')
        }

        pdf = generate_pdf_report(pdf_data)

        return send_file(
            BytesIO(pdf),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"relatorio_{data_inicio}_a_{data_fim}.pdf"
        )

    except Exception as e:
        print(f"Erro ao exportar PDF: {e}")
        return render_template('error.html', message="Erro ao exportar PDF"), 500
    finally:
        conn.close()