from app import db  # Importamos la instancia db desde __init__.py


# app/Model/venta.py
class Venta(db.Model):
    __tablename__ = 'ventas'
    id = db.Column('id_venta', db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'))
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())
    total_pago = db.Column(db.Numeric(12, 2))
    estado_envio = db.Column(db.String(50), default='pendiente')

    # Relación para obtener los productos de esta venta
    detalles = db.relationship('DetalleVenta', backref='venta', lazy=True)

