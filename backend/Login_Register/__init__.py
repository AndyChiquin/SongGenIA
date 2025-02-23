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
    app = Flask(__name__)

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

    # Inicializar rutas OAuth
    init_oauth_routes(auth_bp, google) 

    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix='/login/auth')


    return app
