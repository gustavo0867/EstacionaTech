from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from EstacionaTech.database.database import conectar
#from EstacionaTech.models.setor import listar_todos
import datetime
import sqlite3

configadm_bp = Blueprint('configadm', __name__, template_folder='../templates')


@configadm_bp.route('/configuracoes_admin')
def configuracoes_admin():
    if 'usuario_id' not in session or session.get('tipo') != 'administrador':
        flash('Você não tem permissão para acessar esta página', 'error')
        return redirect(url_for('auth.login'))

    return render_template('configuracoes_admin.html', nome=session.get('nome'))


@configadm_bp.route('/config_setores', methods=['GET', 'POST'])
def config_setores():
    return redirect(url_for('setor.config_setores'))


@configadm_bp.route('/config_vagas', methods=['GET', 'POST'])
def config_vagas():
    return render_template('config_vagas.html')


@configadm_bp.route('/config_tarifas')
def config_tarifas():
    return redirect(url_for('tarifa.config_tarifas'))