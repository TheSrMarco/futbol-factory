from app import db


class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column('id_categoria', db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)