from flask_login import UserMixin
from app import db


class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    # Mapeo: 'id_usuario' en la DB <-> 'id' en Flask/Python
    id = db.Column('id_usuario', db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    # Cambia 'es_admin' por 'rol' para coincidir con tu SQL (admin/cliente/vendedor)
    rol = db.Column(db.String(20), default='cliente')

    def __repr__(self):
        return f'<Usuario {self.email}>'