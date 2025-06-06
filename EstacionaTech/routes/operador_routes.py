from EstacionaTech.controllers.setor_controller import SetorController
from EstacionaTech.controllers.vaga_controller import VagaController
from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash
from EstacionaTech.models.operador import Operador
from datetime import datetime

operador_bp = Blueprint('operadores', __name__, template_folder='../templates')

@operador_bp.route('/painel_operador')
def painel_operador():
    vagas = VagaController.listar_vagas()
    setores = SetorController.listar_setores()
    return render_template('painel_operador.html', vagas=vagas, setores=setores, nome=session.get('nome'))

@operador_bp.route('/config_operadores', methods=['GET', 'POST'])
def config_operadores():
    if 'usuario_id' not in session or session.get('tipo') != 'administrador':
        flash('Acesso negado.', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        id_usuario = request.form['id_usuario']
        cpf_usuario = request.form['cpf_usuario']
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        confirmar_senha = request.form.get('confirmar_senha', '')

        if senha != confirmar_senha:
            flash('Senhas não coincidem.', 'error')
            return redirect(url_for('operadores.config_operadores'))

        hashed_password = generate_password_hash(senha)
        success, message = Operador.create(id_usuario, cpf_usuario, nome, email, hashed_password)
        flash(message, 'success' if success else 'error')

        return redirect(url_for('operadores.config_operadores'))
    
    operadores_originais = Operador.get_all()

    operadores_processados = []

    for operador_tupla in operadores_originais:
        operador_lista = list(operador_tupla)  

        data_ingresso = operador_lista[6]

        if isinstance(data_ingresso, str):
            try:
                operador_lista[6] = datetime.strptime(data_ingresso.split('.')[0], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                print(f"AVISO: Não foi possível converter a data '{data_ingresso}' para o operador {operador_lista[0]}.")
                operador_lista[6] = data_ingresso 
        
        operadores_processados.append(tuple(operador_lista))

    return render_template('config_operadores.html', operadores=operadores_processados, nome=session.get('nome'))


@operador_bp.route('/remover_operador/<id_operador>', methods=['POST'])
def remover_operador(id_operador):
    if 'usuario_id' not in session or session.get('tipo') != 'administrador':
        flash('Acesso negado.', 'error')
        return redirect(url_for('auth.login'))

    success, message = Operador.delete(id_operador)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('operadores.config_operadores'))


@operador_bp.route('/editar_operador', methods=['POST'])
def editar_operador():
    if 'usuario_id' not in session or session.get('tipo') != 'administrador':
        flash('Acesso negado.', 'error')
        return redirect(url_for('auth.login'))

    id_usuario = request.form['id_usuario']
    nome = request.form['nome']
    email = request.form['email']
    cpf_usuario = request.form['cpf_usuario']
    senha = request.form.get('senha', '')

    if senha:
        hashed_password = generate_password_hash(senha)
        success, message = Operador.update(id_usuario, nome, email, cpf_usuario, hashed_password)
    else:
        success, message = Operador.update(id_usuario, nome, email, cpf_usuario)

    flash(message, 'success' if success else 'error')
    return redirect(url_for('operadores.config_operadores'))