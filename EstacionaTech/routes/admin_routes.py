from flask import Blueprint, render_template, session, redirect, url_for

#admin_bp = Blueprint('admin', __name__)
admin_bp = Blueprint('admin', __name__, template_folder='../templates')

@admin_bp.route('/painel_admin')
def painel_admin():
    if 'usuario_id' not in session or session['tipo'] != 'administrador':
        return redirect(url_for('auth.login'))
    return render_template('painel_admin.html', nome=session['nome'])

@admin_bp.route('/configuracoes_admin')
def configuracoes_admin():
    return render_template('configuracoes_admin.html')

# @admin_bp.route('/relatorios')
# def relatorios_admin():
#     return render_template('relatorios.html')

