from flask import Blueprint, render_template, session, redirect, url_for
from EstacionaTech.models.setor import listar_setores


#configadm_bp = Blueprint('configadm', __name__)
configadm_bp = Blueprint('configadm', __name__, template_folder='../templates')


@configadm_bp.route('/configuracoes_admin')
def configuracoes_admin():
    return render_template('configuracoes_admin.html')

@configadm_bp.route('/config_setores', methods=['GET', 'POST'])
def config_setores():
    #return redirect(url_for('setor.config_setores'))
    #return render_template('setor.config_setores.html')
    setores = listar_setores()

    return render_template('config_setores.html', setores=setores)


@configadm_bp.route('/config_vagas')
def config_vagas():
    return render_template('config_vagas.html')


@configadm_bp.route('/config_tarifas')
def config_tarifas():
    return redirect(url_for('tarifa.config_tarifas')) 