# from flask import Blueprint, render_template, request, redirect, url_for, flash, session
# from EstacionaTech.controllers.setor_controller import SetorController
#
# relatorio_bp = Blueprint('relatorio', __name__, template_folder='../templates')
#
#
# @relatorio_bp.route('/gerar_relatorios')
# def gerar_relatorios():
#     relatorios = SetorController.listar_setores()
#     return render_template('config_setores.html', setores=setores)
#
# ------

from flask import Blueprint, render_template, request, session, redirect, url_for, flash, send_file
from datetime import datetime
from io import BytesIO
from EstacionaTech.controllers.relatorio_controller import Relatorio
#from EstacionaTech.relatorios.gerador_pdf import gerar_pdf_relatorio_operacional, gerar_pdf_relatorio_financeiro

relatorio_bp = Blueprint('relatorio', __name__, template_folder='../templates')

@relatorio_bp.route('/gerar_relatorios', methods=['GET', 'POST'])
def relatorios():
    print("Entrou!!!")
    if 'usuario_id' not in session or session['tipo'] != 'administrador':
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        tipo_relatorio = request.form.get('tipo_relatorio')
        data_inicio_str = request.form.get('data_inicio')
        data_fim_str = request.form.get('data_fim')

        if not tipo_relatorio or not data_inicio_str or not data_fim_str:
            flash('Todos os campos são obrigatórios!', 'error')
            return redirect(url_for('admin.painel_admin'))

        try:
            data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d')
            data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d')
        except ValueError:
            flash('Datas inválidas. Use o formato YYYY-MM-DD.')
            return redirect(url_for('relatorio.gerar_relatorios'))

        relatorio = Relatorio()

        # buffer = BytesIO()
        #
        # if tipo_relatorio == 'operacional':
        #     dados = relatorio.listar_infos_operacionais_relevantes(data_inicio, data_fim)
        #     gerar_pdf_relatorio_operacional(buffer, dados, data_inicio, data_fim)
        #
        # elif tipo_relatorio == 'financeiro':
        #     dados = relatorio.listar_infos_financeiras_relevantes(data_inicio, data_fim)
        #     faturamento_total = relatorio.calc_faturamento_total(data_inicio, data_fim)
        #     gerar_pdf_relatorio_financeiro(buffer, dados, data_inicio, data_fim, faturamento_total)
        #
        # else:
        #     flash('Tipo de relatório inválido.')
        #     return redirect(url_for('admin.relatorios'))
        #
        # buffer.seek(0)
        # nome_arquivo = f"{tipo_relatorio}_relatorio_{data_inicio.date()}_{data_fim.date()}.pdf"
        # return send_file(buffer, as_attachment=True, download_name=nome_arquivo, mimetype='application/pdf')

    return render_template('relatorios.html', nome=session['nome'])
