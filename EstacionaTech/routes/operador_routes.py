from flask import Blueprint, render_template, session, redirect, url_for

operador_bp = Blueprint('operador', __name__)

@operador_bp.route('/painel_operador')
def painel_operador():
    if 'usuario_id' not in session or session['tipo'] != 'operador':
        return redirect(url_for('auth.login'))
    return render_template('painel_operador.html', nome=session['nome'])
