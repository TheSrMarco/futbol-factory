from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='Views', static_folder='../static')
    app.config['SECRET_KEY'] = 'mi_llave_super_secreta_123'
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.auth_page'
    login_manager.login_message = "Por favor, inicia sesión para acceder."
    login_manager.login_message_category = "info"

    with app.app_context():
        # Importar modelos UNA SOLA VEZ aquí
        from app.Model.categoria import Categoria
        from app.Model.producto import Producto
        from app.Model.usuario import Usuario
        from app.Model.venta import Venta
        from app.Model.detalle_venta import DetalleVenta
        from app.Model.carrito import Carrito

        db.create_all()

        # Registrar Blueprints
        from app.Controller.main import main_bp
        from app.Controller.auth import auth_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp)

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.Model.usuario import Usuario
    return Usuario.query.get(int(user_id))