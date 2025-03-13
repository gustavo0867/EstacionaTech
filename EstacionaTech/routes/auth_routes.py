from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from EstacionaTech.database.database import verificar_login  # Certifique-se de que está no caminho correto.

# Criando o Blueprint com o mesmo nome que será usado na referência 'auth'
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = verificar_login(email, senha)

        if usuario:
            session['usuario_id'] = usuario[0]
            session['usuario_email'] = usuario[1]  # Exemplo de salvar email na sessão
            session['usuario_tipo'] = usuario[2]  # Supondo que o tipo do usuário está na posição 2 da tupla

            flash('Login realizado com sucesso!', 'success')

            if session['usuario_tipo'] == 'administrador':
                return redirect(url_for('admin.painel'))
            elif session['usuario_tipo'] == 'operador':
                return redirect(url_for('operador.painel'))
            else:
                return redirect(url_for('auth.login'))
        else:
            flash("Email ou senha incorretos!", "danger")
            return render_template("login.html")  # Verifique se o caminho está correto

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Você saiu da conta!", "success")
    return redirect(url_for('auth.login'))
