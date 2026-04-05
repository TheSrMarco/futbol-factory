from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash # Para seguridad
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.Model.usuario import Usuario

auth_bp = Blueprint('auth', __name__)

# --- RUTA LOGIN ---
@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    # remember = True if request.form.get('remember') else False

    # 1. Buscar usuario en BD
    usuario = Usuario.query.filter_by(email=email).first()

    # 2. Verificar si existe y si la contraseña coincide (desencriptando)
    if not usuario or not check_password_hash(usuario.password, password):
        flash('Correo o contraseña incorrectos, intenta de nuevo.', 'danger')
        return redirect(url_for('auth.auth_page')) # Te devuelve al form

    # 3. Si todo ok, iniciamos sesión
    login_user(usuario)
    return redirect(url_for('main.hello_world'))


# --- RUTA REGISTRO ---
@auth_bp.route('/registro', methods=['POST'])
def registro():
    email = request.form.get('email')
    nombre = request.form.get('nombre')
    password = request.form.get('password')

    # 1. Verificar si el correo ya existe
    usuario_existente = Usuario.query.filter_by(email=email).first()

    if usuario_existente:
        flash('Ese correo ya está registrado.', 'warning')
        return redirect(url_for('auth.auth_page'))

    # 2. Crear nuevo usuario (ENCRIPTANDO LA CONTRASEÑA)
    nuevo_usuario = Usuario(
        email=email,
        nombre=nombre,
        password=generate_password_hash(password, method='pbkdf2:sha256') # Seguridad
    )

    # 3. Guardar en BD
    db.session.add(nuevo_usuario)
    db.session.commit()

    flash('Cuenta creada exitosamente. ¡Ahora inicia sesión!', 'success')
    return redirect(url_for('auth.auth_page')) # Te devuelve para que te loguees


# --- RUTA PARA MOSTRAR LA VISTA ---
# En app/Controller/auth.py
@auth_bp.route('/auth', methods=['GET'])
def auth_page():
    if current_user.is_authenticated:
        return redirect(url_for('main.hello_world'))
    # Asegúrate de que este nombre sea el correcto:
    return render_template('inicioregistro.html')





@auth_bp.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    # Limpiar explícitamente la sesión de Flask por seguridad extra
    from flask import session
    session.clear()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('auth.auth_page')) # Redirigir al formulario de login