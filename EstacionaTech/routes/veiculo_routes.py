from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from EstacionaTech.controllers.veiculo_controller import VeiculoController
from EstacionaTech.controllers.cliente_controller import ClienteController

veiculo_bp = Blueprint('veiculo', __name__, template_folder='../templates')


@veiculo_bp.route('/gerenciar_clientes')
def gerenciar_clientes():
    """Página de gerenciamento de clientes e veículos (operadores)"""
    if 'usuario_id' not in session:
        flash('Você precisa fazer login para acessar esta página.', 'error')
        return redirect(url_for('auth.login'))

    # Buscar clientes com seus veículos
    clientes = ClienteController.listar_clientes()

    return render_template(
        'gerenciar_clientes.html',
        clientes=clientes,
        nome=session.get('nome')
    )


@veiculo_bp.route('/adicionar_cliente', methods=['POST'])
def adicionar_cliente():
    """Adiciona um novo cliente"""
    if 'usuario_id' not in session:
        flash('Você precisa fazer login para realizar esta operação.', 'error')
        return redirect(url_for('auth.login'))

    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    telefone = request.form.get('telefone')
    email = request.form.get('email')
    mensalista = request.form.get('mensalista', '0')
    modalidade = request.form.get('modalidade', 'casual')

    # Converter mensalista para inteiro (0 = não mensalista, 1 = mensalista)
    mensalista = 1 if mensalista == '1' else 0

    if not nome or not cpf or not telefone or not email:
        flash('Nome, CPF, telefone e email são obrigatórios.', 'error')
        return redirect(url_for('veiculo.gerenciar_clientes'))

    # Verificar se o cliente já existe
    cliente_existente = ClienteController.buscar_por_cpf(cpf)
    if cliente_existente:
        flash('CPF já cadastrado.', 'error')
        return redirect(url_for('veiculo.gerenciar_clientes'))

    # Adicionar cliente
    sucesso = ClienteController.criar_cliente(nome, cpf, telefone, email, mensalista, modalidade)

    if sucesso:
        flash('Cliente adicionado com sucesso!', 'success')
    else:
        flash('Erro ao adicionar cliente.', 'error')

    return redirect(url_for('veiculo.gerenciar_clientes'))


@veiculo_bp.route('/editar_cliente/<int:id_cliente>', methods=['POST'])
def editar_cliente(id_cliente):
    """Edita um cliente existente"""
    if 'usuario_id' not in session:
        flash('Você precisa fazer login para realizar esta operação.', 'error')
        return redirect(url_for('auth.login'))

    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    telefone = request.form.get('telefone')
    email = request.form.get('email')
    mensalista = request.form.get('mensalista', '0')
    modalidade = request.form.get('modalidade', 'casual')

    # Converter mensalista para inteiro (0 = não mensalista, 1 = mensalista)
    mensalista = 1 if mensalista == '1' else 0

    if not nome or not cpf:
        flash('Nome e CPF são obrigatórios.', 'error')
        return redirect(url_for('veiculo.gerenciar_clientes'))

    # Editar cliente
    sucesso = ClienteController.editar_cliente(id_cliente, nome, cpf, telefone, email, mensalista, modalidade)

    if sucesso:
        flash('Cliente atualizado com sucesso!', 'success')
    else:
        flash('Erro ao atualizar cliente.', 'error')

    return redirect(url_for('veiculo.gerenciar_clientes'))


@veiculo_bp.route('/excluir_cliente/<int:id_cliente>')
def excluir_cliente(id_cliente):
    """Remove um cliente"""
    if 'usuario_id' not in session:
        flash('Você precisa fazer login para realizar esta operação.', 'error')
        return redirect(url_for('auth.login'))

    # Verificar se o cliente possui veículos
    veiculos = VeiculoController.listar_por_cliente(id_cliente)
    if veiculos:
        flash('Não é possível excluir este cliente pois possui veículos cadastrados.', 'error')
        return redirect(url_for('veiculo.gerenciar_clientes'))

    # Excluir cliente
    sucesso = ClienteController.excluir_cliente(id_cliente)

    if sucesso:
        flash('Cliente excluído com sucesso!', 'success')
    else:
        flash('Erro ao excluir cliente.', 'error')

    return redirect(url_for('veiculo.gerenciar_clientes'))

@veiculo_bp.route('/adicionar_veiculo', methods=['POST'])
def adicionar_veiculo():
    """Adiciona um novo veículo"""
    if 'usuario_id' not in session:
        flash('Você precisa fazer login para realizar esta operação.', 'error')
        return redirect(url_for('auth.login'))

    placa = request.form.get('placa')
    modelo = request.form.get('modelo')
    marca = request.form.get('marca')
    cor = request.form.get('cor')
    ano_fabricacao = request.form.get('ano_fabricacao')
    id_cliente = request.form.get('id_cliente')

    if not placa or not modelo or not id_cliente:
        flash('Placa, modelo e cliente são obrigatórios.', 'error')
        return redirect(url_for('veiculo.gerenciar_clientes'))

    # Verificar se o veículo já existe
    veiculo_existente = VeiculoController.obter_veiculo(placa)
    if veiculo_existente:
        flash('Veículo com esta placa já cadastrado.', 'error')
        return redirect(url_for('veiculo.gerenciar_clientes'))

    # Adicionar veículo
    sucesso = VeiculoController.criar_veiculo(placa, modelo, marca, cor, ano_fabricacao, id_cliente)

    if sucesso:
        flash('Veículo adicionado com sucesso!', 'success')
    else:
        flash('Erro ao adicionar veículo.', 'error')

    return redirect(url_for('veiculo.gerenciar_clientes'))


@veiculo_bp.route('/editar_veiculo/<placa>', methods=['POST'])
def editar_veiculo(placa):
    """Edita um veículo existente"""
    if 'usuario_id' not in session:
        flash('Você precisa fazer login para realizar esta operação.', 'error')
        return redirect(url_for('auth.login'))

    modelo = request.form.get('modelo')
    marca = request.form.get('marca')
    cor = request.form.get('cor')
    ano_fabricacao = request.form.get('ano_fabricacao')
    id_cliente = request.form.get('id_cliente')

    if not modelo or not id_cliente:
        flash('Modelo e cliente são obrigatórios.', 'error')
        return redirect(url_for('veiculo.gerenciar_clientes'))

    # Editar veículo
    sucesso = VeiculoController.editar_veiculo(placa, modelo, marca, cor, ano_fabricacao, id_cliente)

    if sucesso:
        flash('Veículo atualizado com sucesso!', 'success')
    else:
        flash('Erro ao atualizar veículo.', 'error')

    return redirect(url_for('veiculo.gerenciar_clientes'))


@veiculo_bp.route('/excluir_veiculo/<placa>')
def excluir_veiculo(placa):
    """Remove um veículo"""
    if 'usuario_id' not in session:
        flash('Você precisa fazer login para realizar esta operação.', 'error')
        return redirect(url_for('auth.login'))

    # Verificar se o veículo está em uso
    # (Você deve implementar esta verificação no controller)

    # Excluir veículo
    sucesso = VeiculoController.excluir_veiculo(placa)

    if sucesso:
        flash('Veículo excluído com sucesso!', 'success')
    else:
        flash('Erro ao excluir veículo.', 'error')

    return redirect(url_for('veiculo.gerenciar_clientes'))