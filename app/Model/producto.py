from app import db


class Producto(db.Model):
    __tablename__ = 'productos'

    id_producto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Numeric(12, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    imagen_url = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)  # <-- Agrega esto

    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias.id_categoria', ondelete='SET NULL'))

    # Esta columna ya existe en tu DB (por eso el error 42701),
    # ahora la declaramos aquí para que SQLAlchemy la vea:
    id_vendedor = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario', ondelete='CASCADE'))

    # RELACIONES:
    categoria = db.relationship('Categoria', backref=db.backref('productos', lazy=True))

    # IMPORTANTE: Cambia 'Usuarios' por 'Usuario' (o como se llame tu CLASE en usuario.py)
    vendedor = db.relationship('Usuario', backref=db.backref('mis_productos', lazy=True))

    def __repr__(self):
        return f'<Producto {self.nombre} - ${self.precio}>'