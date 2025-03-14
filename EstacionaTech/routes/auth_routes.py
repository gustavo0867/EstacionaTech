from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from EstacionaTech.database.database import verificar_login  # Certifique-se de que está no caminho correto.

# Criando o Blueprint com o mesmo nome que será usado na referência 'auth'
#auth_bp = Blueprint('auth', __name__)
auth_bp = Blueprint('auth', __name__, template_folder='../templates')

@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = verificar_login(email, senha)

        if usuario:
            session['usuario_id'] = usuario[0]
            session['nome'] = usuario[2]
            session['tipo'] = usuario[5]

            if usuario[5] == 'administrador':
                return redirect(url_for('admin.painel_admin'))
            else:
                return redirect(url_for('operador.painel_operador'))
        else:
            flash('Email ou senha inválidos!', 'error')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
