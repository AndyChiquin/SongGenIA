

from flask import Flask
from flask_cors import CORS
from Login_Register.database import db, init_db
from Login_Register.passport import init_passport
from Login_Register.auth import auth_bp, init_oauth_routes  # Importamos correctamente el blueprint
import os
from flask_session import Session
from datetime import timedelta

def create_app():
    """Crea y configura la aplicación Flask"""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Configuración básica
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

    # Inicializar extensiones
    CORS(app)
    Session(app)

    # Inicializar base de datos
    init_db(app)

    # Inicializar autenticación
    google = init_passport(app)

    # Inicializar rutas OAuth (aquí ya puedes registrar las rutas del OAuth)
    init_oauth_routes(google)

    # Registrar blueprints después de inicializar todas las rutas
    app.register_blueprint(auth_bp, url_prefix='/login/auth')

    # Rutas para servir archivos estáticos
    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    @app.route('/login')
    def login_page():
        return app.send_static_file('views/login.html')

    @app.route('/register')
    def register_page():
        return app.send_static_file('views/register.html')

    @app.route('/dashboard')
    def dashboard_page():
        return app.send_static_file('views/dashboard.html')

    return app
