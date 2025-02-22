from Login_Register.database import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    cedula = db.Column(db.String(20), unique=True, nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    
    def to_dict(self):
        """Convierte el objeto User a un diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'cedula': self.cedula,
            'telefono': self.telefono,
            'email': self.email,
            'username': self.username
        }