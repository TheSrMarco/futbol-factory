from app import db


class Carrito(db.Model):
    __tablename__ = 'carrito'
    id_carrito = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'))
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'))
    cantidad = db.Column(db.Integer, default=1)

    # ESTA LÍNEA ES CLAVE
    producto = db.relationship('Producto', backref='items_carrito')