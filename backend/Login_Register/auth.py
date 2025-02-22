from flask import Blueprint, session, redirect, url_for
from Login_Register.auth_controller import register, login, google_callback
from flask_login import login_required, logout_user

# Crear blueprint para las rutas de autenticación
auth_bp = Blueprint('auth', __name__)

# Rutas para el registro y login con credenciales
auth_bp.route('/register', methods=['POST'])(register)
auth_bp.route('/login', methods=['POST'])(login)

def init_oauth_routes(google):
    """Inicializa las rutas para autenticación con Google"""
    
    @auth_bp.route('/google')
    def google_login():
        redirect_uri = url_for('auth.google_auth_callback', _external=True)
        return google.authorize_redirect(redirect_uri)
    
    @auth_bp.route('/google/callback')
    def google_auth_callback():
        return google_callback(google)
    
    @auth_bp.route('/logout')
    @login_required
    def logout():
        logout_user()
        session.clear()
        return redirect('/')