from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from EstacionaTech.controllers.locacao_controller import LocacaoController
from EstacionaTech.controllers.veiculo_controller import VeiculoController
from EstacionaTech.controllers.pagamento_controller import PagamentoController
import datetime

locacao_bp = Blueprint('locacao', __name__, template_folder='../templates')

@locacao_bp.route('/operacoes')
def operacoes():
    """Página principal de operações de entrada e saída"""
    if 'usuario_id' not in session:
        flash('Você precisa fazer login para acessar esta página.', 'error')
        return redirect(url_for('auth.login'))

    # Buscar vagas disponíveis
    vagas_disponiveis = LocacaoController.listar_vagas_disponiveis()

    # Buscar locações ativas (veículos no estacionamento)
    locacoes_ativas = LocacaoController.listar_ativas()

    # Buscar histórico recente
    historico_recente = LocacaoController.listar_recentes(limit=5)

    return render_template(
        'operacoes.html',
        vagas_disponiveis=vagas_disponiveis,
        locacoes_ativas=locacoes_ativas,
        historico_recente=historico_recente,
        nome=session.get('nome')
    )


@locacao_bp.route('/registrar_entrada', methods=['POST'])
def registrar_entrada():
    """Registra a entrada de um veículo"""
    if 'usuario_id' not in session:
        flash('Você precisa fazer login para realizar esta operação.', 'error')
        return redirect(url_for('auth.login'))

    id_vaga = request.form.get('id_vaga')
    placa = request.form.get('placa')

    if not id_vaga or not placa:
        flash('Vaga e placa do veículo são obrigatórios!', 'error')
        return redirect(url_for('locacao.operacoes'))

    # Verificar se o veículo está cadastrado
    veiculo = VeiculoController.obter_veiculo(placa)

    if not veiculo:
        # Redirecionar para cadastro de veículo
        flash('Veículo não cadastrado. Faça o cadastro primeiro.', 'error')
        # Aqui você poderia redirecionar para uma página de cadastro rápido
        return redirect(url_for('locacao.operacoes'))

    # Registrar entrada
    success, message = LocacaoController.registrar_entrada(
        id_vaga,
        placa,
        session['usuario_id']
    )

    flash(message, 'success' if success else 'error')
    return redirect(url_for('locacao.operacoes'))


@locacao_bp.route('/registrar_saida/<int:id_locacao>', methods=['GET'])
def registrar_saida(id_locacao):
    """Página de confirmação de saída e pagamento"""
    if 'usuario_id' not in session:
        flash('Você precisa fazer login para realizar esta operação.', 'error')
        return redirect(url_for('auth.login'))

    # Buscar dados da locação
    locacao = LocacaoController.buscar_locacao(id_locacao)

    if not locacao:
        flash('Locação não encontrada!', 'error')
        return redirect(url_for('locacao.operacoes'))

    # Converter locacao em lista mutável
    locacao = list(locacao)

    # Garantir que locacao[3] seja datetime
    entrada = locacao[3]
    if isinstance(entrada, str):
        try:
            entrada = datetime.datetime.fromisoformat(entrada.replace(' ', 'T'))
        except ValueError:
            entrada = None  # Ou pode definir uma data padrão/fallback

    locacao[3] = entrada

    # Calcular valor estimado
    valor_estimado = {
        'horas': 1,
        'valor': 0
    }


    if locacao[4] is None:  # Verificar se data_hora_saida está vazia
        agora = datetime.datetime.now()
        minutos_totais = 0
        if entrada:
            minutos_totais = (agora - entrada).total_seconds() / 60

        # Buscar tarifa e tolerância
        tarifa = 5.0  # Valor padrão
        tolerancia_minutos = 15  # Tolerância padrão de segurança

        try:
            from EstacionaTech.database.database import conectar
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT valor_por_hora, tempo_tolerancia FROM Tarifa LIMIT 1")
            result = cursor.fetchone()
            if result:
                tarifa, tolerancia_minutos = result
            conn.close()
        except Exception as e:
            print(f"[ERRO] Erro ao buscar tarifa e tolerância: {e}")

        if minutos_totais <= tolerancia_minutos:
            horas_cobradas = 0
            valor_cobrado = 0.0
        else:
            horas = minutos_totais / 60
            horas_cobradas = max(1, int(horas) + (1 if horas % 1 > 0 else 0))
            valor_cobrado = horas_cobradas * tarifa

        valor_estimado = {
            'horas': horas_cobradas,
            'valor': valor_cobrado
        }

        return render_template(
            'confirmar_saida.html',
            locacao=locacao,
            valor_estimado=valor_estimado,
            nome=session.get('nome')
        )

@locacao_bp.route('/confirmar_saida', methods=['POST'])
def confirmar_saida():
    """Confirma a saída do veículo e registra pagamento"""
    if 'usuario_id' not in session:
        flash('Você precisa fazer login para realizar esta operação.', 'error')
        return redirect(url_for('auth.login'))

    id_locacao = request.form.get('id_locacao')
    forma_pagamento = request.form.get('forma_pagamento', 'dinheiro')

    if not id_locacao:
        flash('ID da locação não fornecido!', 'error')
        return redirect(url_for('locacao.operacoes'))

    # Registrar saída
    success, message, dados_pagamento = LocacaoController.registrar_saida(
        id_locacao,
        session['usuario_id']
    )

    if success:

        if(dados_pagamento == 0):

            flash("Saída registrada com sucesso! Nenhum valor foi cobrado, pois o tempo de permanência ficou dentro da tolerância.", 'success')

        else:
            # Registrar pagamento
            PagamentoController.registrar_pagamento(
                id_locacao=id_locacao,
                id_operador=session['usuario_id'],
                valor=dados_pagamento['valor'],
                forma_pagamento=forma_pagamento
            )

            flash(f"Saída registrada com sucesso! Valor cobrado: R$ {dados_pagamento['valor']:.2f}", 'success')
    else:
        flash(message, 'error')

    return redirect(url_for('locacao.operacoes'))


@locacao_bp.route('/buscar_veiculo', methods=['POST'])
def buscar_veiculo():
    """Busca um veículo pela placa"""
    if 'usuario_id' not in session:
        flash('Você precisa fazer login para realizar esta operação.', 'error')
        return redirect(url_for('auth.login'))

    placa = request.form.get('placa_busca', '')

    if not placa:
        flash('Informe uma placa para buscar!', 'error')
        return redirect(url_for('locacao.operacoes'))

    locacoes = LocacaoController.buscar_por_placa(placa)

    # Buscar vagas disponíveis
    vagas_disponiveis = LocacaoController.listar_vagas_disponiveis()

    # Buscar histórico recente
    historico_recente = LocacaoController.listar_recentes(limit=5)

    if not locacoes:
        flash(f'Nenhum veículo com placa contendo "{placa}" encontrado estacionado no momento.', 'error')

    return render_template(
        'operacoes.html',
        vagas_disponiveis=vagas_disponiveis,
        locacoes_ativas=locacoes,
        historico_recente=historico_recente,
        nome=session.get('nome'),
        busca_realizada=True,
        termo_busca=placa
    )