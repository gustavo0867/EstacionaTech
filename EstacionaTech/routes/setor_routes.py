from flask import Blueprint, render_template
from EstacionaTech.controllers.setor_controller import SetorController

setor_bp = Blueprint('setor', __name__)

@setor_bp.route('/setores')
def listar_setores():
    setores = SetorController.listar_setores()
    return render_template('config_setores.html', setores=setores)
