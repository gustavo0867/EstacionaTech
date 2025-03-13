from flask import Flask, render_template, request, redirect, url_for, session, flash
from EstacionaTech.database.database import verificar_login
from werkzeug.security import generate_password_hash

# Importando os Blueprints
from EstacionaTech.routes.auth_routes import auth_bp
from EstacionaTech.routes.admin_routes import admin_bp
from EstacionaTech.routes.operador_routes import operador_bp
from EstacionaTech.routes.setor_routes import setor_bp
from EstacionaTech.routes.vaga_routes import vaga_bp
from EstacionaTech.controllers.tarifa_controller import tarifa_bp

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.secret_key = 'chave_secreta_super_segura'

    # Definindo rota principal
    @app.route('/')
    def home():
        return redirect(url_for('auth.login'))

    # Registrando os Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    # app.register_blueprint(admin_bp, url_prefix='/admin')
    # app.register_blueprint(operador_bp, url_prefix='/operador')
    # app.register_blueprint(setor_bp, url_prefix='/setor')
    # app.register_blueprint(vaga_bp, url_prefix='/vaga')
    # app.register_blueprint(tarifa_bp, url_prefix='/tarifa')

    return app  # Retorna a instância do Flask

if __name__ == '__main__':
    app = create_app()  # Criando a instância da aplicação
    app.run(debug=True)
