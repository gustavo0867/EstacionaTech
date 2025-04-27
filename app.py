from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash
import sys
from pathlib import Path

# Adiciona o diretório raiz ao Python Path
sys.path.append(str(Path(__file__).parent))

# Configuração do Flask
app = Flask(__name__, static_folder='EstacionaTech/static', template_folder='EstacionaTech/templates')
app.secret_key = 'chave_secreta_super_segura'

# Importação dos Blueprints DEPOIS da criação do app
from EstacionaTech.routes.auth_routes import auth_bp
from EstacionaTech.routes.admin_routes import admin_bp
from EstacionaTech.routes.operador_routes import operador_bp
from EstacionaTech.routes.configadm_routes import configadm_bp
from EstacionaTech.routes.tarifa_routes import tarifa_bp
from EstacionaTech.routes.setor_routes import setor_bp
from EstacionaTech.routes.vaga_routes import vaga_bp
from EstacionaTech.routes.locacao_routes import locacao_bp
from EstacionaTech.routes.cliente_routes import cliente_bp
from EstacionaTech.controllers.relatorio_controller import relatorio_bp

# Registrando os blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(operador_bp, url_prefix='/operador')
app.register_blueprint(configadm_bp, url_prefix='/configadm')
app.register_blueprint(tarifa_bp, url_prefix='/tarifa')
app.register_blueprint(setor_bp, url_prefix='/setor')
app.register_blueprint(vaga_bp, url_prefix='/vaga')
app.register_blueprint(cliente_bp, url_prefix='/cliente')
app.register_blueprint(locacao_bp, url_prefix='/locacao')
app.register_blueprint(relatorio_bp, url_prefix='/relatorios')

# Definindo rota principal
@app.route('/')
def home():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True)