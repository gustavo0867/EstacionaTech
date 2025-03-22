from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from EstacionaTech.controllers.vaga_controller import VagaController
from EstacionaTech.controllers.setor_controller import SetorController


vaga_bp = Blueprint('vaga', __name__, template_folder='../templates')

@vaga_bp.route('/config_vagas')
def config_vagas():
    vagas = VagaController.listar_vagas()
    setores = SetorController.listar_setores()
    print(setores)
    return render_template('config_vagas.html', vagas=vagas, setores=setores)

@vaga_bp.route('/adicionar_vaga', methods=['POST'])
def adicionar_vaga():


    if 'usuario_id' not in session or session['tipo'] != 'administrador':
        flash('Você não tem permissão para realizar esta ação.', 'error')
        return redirect(url_for('auth.login'))
    #setor, tipo, status

    id_vaga = request.form.get('id_vaga')
    setor = request.form.get('setor')
    tipo = request.form.get('tipo')
    status = request.form.get('status')

    if not id_vaga or not setor or not tipo or not status:
        flash('Todos os campos são obrigatórios!', 'error')
        return redirect(url_for('setor.config_vagas'))

    try:
        result = VagaController.criar_vaga(id_vaga, setor, tipo, status)
        if result:
            flash(f'Vaga {id_vaga} adicionada com sucesso!', 'success')
        else:
            flash('Erro ao adicionar Vaga. Verifique se o ID já existe.', 'error')
    except ValueError:
        flash('Os campos digitados devem ser válidos!', 'error')

    return redirect(url_for('vaga.config_vagas'))
    #return render_template('vaga.config_vagas', setores=setores)



@vaga_bp.route('/editar_vaga', methods=['POST'])
def editar_vaga():
    if 'usuario_id' not in session or session['tipo'] != 'administrador':
        flash('Você não tem permissão para realizar esta ação.', 'error')
        return redirect(url_for('auth.login'))

    id_vaga = request.form.get('id_vaga')
    setor = request.form.get('setor')
    tipo = request.form.get('tipo')
    status = request.form.get('status')

    if not id_vaga or not setor or not tipo or not status:
        flash('Todos os campos são obrigatórios!', 'error')
        return redirect(url_for('vaga.config_vagas'))

    try:
        result = VagaController.editar_vaga(id_vaga, setor, tipo, status)
        if result:
            flash(f'Vaga {id_vaga} atualizado com sucesso!', 'success')
        else:
            flash('Erro ao atualizar vaga. Verifique se a vaga existe.', 'error')
    except ValueError:
        flash('Os campos digitados devem ser válidos!', 'error')

    return redirect(url_for('vaga.config_vaga'))


@vaga_bp.route('/remover_vaga', methods=['POST'])
def remover_vaga():
    if 'usuario_id' not in session or session['tipo'] != 'administrador':
        flash('Você não tem permissão para realizar esta ação.', 'error')
        return redirect(url_for('auth.login'))

    id_vaga = request.form.get('id_vaga')

    if not id_vaga:
        flash('ID da vaga não fornecido!', 'error')
        return redirect(url_for('vaga.config_vagas'))

    result = VagaController.excluir_vaga(id_vaga)
    if result:
        flash(f'Vaga {id_vaga} removido com sucesso!', 'success')
    else:
        flash('Erro ao remover vaga. Verifique se a vaga existe', 'error')

    return redirect(url_for('vaga.config_vagas'))
