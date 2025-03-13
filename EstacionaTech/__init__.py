from flask import Flask
from EstacionaTech.routes.auth_routes import auth_bp
from EstacionaTech.routes.admin_routes import admin_bp
from EstacionaTech.routes.operador_routes import operador_bp
from EstacionaTech.routes.setor_routes import setor_bp
from EstacionaTech.routes.vaga_routes import vaga_bp
from EstacionaTech.controllers.tarifa_controller import tarifa_bp

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.secret_key = 'chave_secreta_super_segura'

    # Registrando os Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(operador_bp)
    app.register_blueprint(setor_bp)
    app.register_blueprint(vaga_bp)
    app.register_blueprint(tarifa_bp)

    return app
