from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from EstacionaTech.controllers.setor_controller import SetorController

setor_bp = Blueprint('setor', __name__, template_folder='../templates')


@setor_bp.route('/config_setores')
def config_setores():
    setores = SetorController.listar_setores()
    return render_template('config_setores.html', setores=setores)


@setor_bp.route('/adicionar_setor', methods=['POST'])
def adicionar_setor():
    if 'usuario_id' not in session or session['tipo'] != 'administrador':
        flash('Você não tem permissão para realizar esta ação.', 'error')
        return redirect(url_for('auth.login'))

    id_setor = request.form.get('id_setor')
    n_vagas = request.form.get('n_vagas')

    if not id_setor or not n_vagas:
        flash('Todos os campos são obrigatórios!', 'error')
        return redirect(url_for('setor.config_setores'))

    try:
        n_vagas = int(n_vagas)
        if n_vagas <= 0:
            flash('O número de vagas deve ser maior que zero!', 'error')
            return redirect(url_for('setor.config_setores'))

        result = SetorController.criar_setor(id_setor, n_vagas)
        if result:
            flash(f'Setor {id_setor} adicionado com sucesso!', 'success')
        else:
            flash('Erro ao adicionar setor. Verifique se o ID já existe.', 'error')
    except ValueError:
        flash('O número de vagas deve ser um número válido!', 'error')

    return redirect(url_for('setor.config_setores'))


@setor_bp.route('/editar_setor', methods=['POST'])
def editar_setor():
    if 'usuario_id' not in session or session['tipo'] != 'administrador':
        flash('Você não tem permissão para realizar esta ação.', 'error')
        return redirect(url_for('auth.login'))

    id_setor = request.form.get('id_setor')
    n_vagas = request.form.get('n_vagas')

    if not id_setor or not n_vagas:
        flash('Todos os campos são obrigatórios!', 'error')
        return redirect(url_for('setor.config_setores'))

    try:
        n_vagas = int(n_vagas)
        if n_vagas <= 0:
            flash('O número de vagas deve ser maior que zero!', 'error')
            return redirect(url_for('setor.config_setores'))

        result = SetorController.editar_setor(id_setor, n_vagas)
        if result:
            flash(f'Setor {id_setor} atualizado com sucesso!', 'success')
        else:
            flash('Erro ao atualizar setor. Verifique se o setor existe.', 'error')
    except ValueError:
        flash('O número de vagas deve ser um número válido!', 'error')

    return redirect(url_for('setor.config_setores'))


@setor_bp.route('/remover_setor', methods=['POST'])
def remover_setor():
    if 'usuario_id' not in session or session['tipo'] != 'administrador':
        flash('Você não tem permissão para realizar esta ação.', 'error')
        return redirect(url_for('auth.login'))

    id_setor = request.form.get('id_setor')

    if not id_setor:
        flash('ID do setor não fornecido!', 'error')
        return redirect(url_for('setor.config_setores'))

    result = SetorController.excluir_setor(id_setor)
    if result:
        flash(f'Setor {id_setor} removido com sucesso!', 'success')
    else:
        flash('Erro ao remover setor. Verifique se o setor existe e não tem vagas associadas.', 'error')

    return redirect(url_for('setor.config_setores'))