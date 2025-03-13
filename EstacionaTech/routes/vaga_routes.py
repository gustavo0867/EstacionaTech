from flask import Blueprint, render_template

vaga_bp = Blueprint('vaga', __name__)

@vaga_bp.route('/config_vagas')
def config_vagas():
    return render_template('config_vagas.html')
