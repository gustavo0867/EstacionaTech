from flask import Flask, render_template, request, redirect, url_for, session, flash
from database.database import verificar_login
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = 'chave_secreta_super_segura'


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
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
                return redirect(url_for('painel_admin'))
            else:
                return redirect(url_for('painel_operador'))
        else:
            flash('Email ou senha inválidos!', 'error')

    return render_template('login.html')


@app.route('/painel_admin')
def painel_admin():
    if 'usuario_id' not in session or session['tipo'] != 'administrador':
        return redirect(url_for('login'))
    return render_template('painel_admin.html', nome=session['nome'])


@app.route('/painel_operador')
def painel_operador():
    if 'usuario_id' not in session or session['tipo'] != 'operador':
        return redirect(url_for('login'))
    return render_template('painel_operador.html', nome=session['nome'])


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/configuracoes_admin')
def configuracoes_admin():
    return render_template('configuracoes_admin.html')

@app.route('/config_setores')
def config_setores():
    return render_template('config_setores.html')
@app.route('/config_vagas')
def config_vagas():
    return render_template('config_vagas.html')

@app.route('/config_tarifas')
def config_tarifas():
    return render_template('config_tarifas.html')

if __name__ == '__main__':
    app.run(debug=True)