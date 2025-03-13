from flask import Flask
from flask import Flask, render_template, request, redirect, url_for, session, flash
from EstacionaTech.database.database import verificar_login
from werkzeug.security import generate_password_hash

# Importando os Blueprints
from EstacionaTech.routes.auth_routes import auth_bp
from EstacionaTech.routes.admin_routes import admin_bp
from EstacionaTech.routes.operador_routes import operador_bp
from EstacionaTech.routes.configadm_routes import configadm_bp
from EstacionaTech.routes.tarifa_routes import tarifa_bp
from EstacionaTech.routes.setor_routes import setor_bp
from EstacionaTech.routes.vaga_routes import vaga_bp


app = Flask(__name__, static_folder='EstacionaTech/static', template_folder='EstacionaTech/templates')

#app = Flask(__name__)
app.secret_key = 'chave_secreta_super_segura'


    # Definindo rota principal
@app.route('/')
def home():
    return redirect(url_for('auth.login'))


app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(operador_bp, url_prefix='/operador')
app.register_blueprint(configadm_bp, url_prefix='/configadm')
app.register_blueprint(tarifa_bp, url_prefix='/tarifa')


    





if __name__ == '__main__':
    app.run(debug=True)