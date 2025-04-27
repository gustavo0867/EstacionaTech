from flask import Flask
from controllers.relatorio_controller import relatorio_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(relatorio_bp)
    return app

# Este arquivo pode ficar vazio ou conter inicializações comuns, se necessário.
# Se desejar, pode definir variáveis globais para os blueprints aqui.
