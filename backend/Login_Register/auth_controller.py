import os
import jwt
import bcrypt
from flask import jsonify, request, session, redirect, url_for
from Login_Register.user import User
from Login_Register.database import db

def register():
    """Registra un nuevo usuario"""
    data = request.json
    nombre = data.get('nombre')
    cedula = data.get('cedula')
    telefono = data.get('telefono')
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    
    # Verificar que todos los campos estén presentes
    if not all([nombre, cedula, telefono, email, password, username]):
        return jsonify({"msg": "Todos los campos son obligatorios"}), 400
    
    # Encriptar contraseña
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    try:
        # Crear nuevo usuario
        new_user = User(
            nombre=nombre,
            cedula=cedula,
            telefono=telefono,
            email=email,
            password=hashed_password,
            username=username
        )
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({"msg": "Usuario registrado correctamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error al registrar el usuario", "error": str(e)}), 500

def login():
    """Inicia sesión de un usuario"""
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    # Buscar usuario por email
    user = User.query.filter_by(email=email).first()
    
    # Verificar si existe el usuario y la contraseña es correcta
    if not user or not user.password or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({"msg": "Credenciales inválidas"}), 401
    
    # Generar token JWT
    token = jwt.encode(
        {"id": user.id, "email": user.email},
        os.getenv('SECRET_KEY'),
        algorithm="HS256"
    )
    
    return jsonify({"token": token, "user": user.to_dict()})

def google_callback(google):
    """Callback después de la autenticación con Google"""
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    
    # Buscar usuario por email o crearlo si no existe
    user = User.query.filter_by(email=user_info['email']).first()
    if not user:
        user = User(
            nombre=user_info['name'],
            cedula=None,
            telefono=None,
            email=user_info['email'],
            password=None,
            username=user_info['name']
        )
        db.session.add(user)
        db.session.commit()
    
    # Guardar información del usuario en la sesión
    session['user_id'] = user.id
    
    return redirect('/dashboard')