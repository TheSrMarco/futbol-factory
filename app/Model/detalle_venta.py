from app import db


class DetalleVenta(db.Model):
    __tablename__ = 'detalle_venta'

    # ESTA LÍNEA ARREGLA EL ERROR
    __table_args__ = {'extend_existing': True}

    id = db.Column('id_detalle', db.Integer, primary_key=True)
    id_venta = db.Column(db.Integer, db.ForeignKey('ventas.id_venta'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(12, 2), nullable=False)

    producto = db.relationship('Producto')