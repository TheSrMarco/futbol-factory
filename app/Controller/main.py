from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.Model.producto import Producto
from app.Model.venta import Venta
from app.Model.categoria import Categoria
from app.Model.carrito import Carrito
from app.Model.detalle_venta import DetalleVenta
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def hello_world():
    # Añadimos .filter_by(activo=True) antes del ordenamiento
    productos_tendencia = Producto.query.filter_by(activo=True)\
                                  .order_by(Producto.id_producto.desc())\
                                  .limit(3).all()
    return render_template('index.html', productos=productos_tendencia)

@main_bp.route('/catalogo')
def catalogo():
    categoria_id = request.args.get('cat', type=int)

    # Filtramos para que SOLO aparezcan productos con activo=True
    if categoria_id:
        lista_productos = Producto.query.filter_by(
            id_categoria=categoria_id,
            activo=True
        ).all()
    else:
        lista_productos = Producto.query.filter_by(activo=True).all()

    categorias = Categoria.query.all()
    return render_template('catalogo.html', productos=lista_productos, categorias=categorias)


@main_bp.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html', usuario=current_user)


@main_bp.route('/mis-compras')
@login_required
def mis_compras():
    compras = Venta.query.filter_by(id_usuario=current_user.id).order_by(Venta.fecha.desc()).all()
    return render_template('mis_compras.html', compras=compras)


@main_bp.route('/carrito/agregar/<int:id_producto>', methods=['POST'])
@login_required
def agregar_al_carrito(id_producto):
    item = Carrito.query.filter_by(id_usuario=current_user.id, id_producto=id_producto).first()
    if item:
        item.cantidad += 1
    else:
        nuevo_item = Carrito(id_usuario=current_user.id, id_producto=id_producto, cantidad=1)
        db.session.add(nuevo_item)
    db.session.commit()
    flash('Producto añadido al carrito.', 'success')
    return redirect(url_for('main.catalogo'))


@main_bp.route('/carrito')
@login_required
def ver_carrito():
    items = Carrito.query.filter_by(id_usuario=current_user.id).order_by(Carrito.id_carrito.asc()).all()
    total = sum(item.producto.precio * item.cantidad for item in items)
    return render_template('carrito.html', items=items, total=total)


@main_bp.route('/carrito/sumar/<int:id_producto>', methods=['POST'])
@login_required
def sumar_cantidad(id_producto):
    item = Carrito.query.filter_by(id_usuario=current_user.id, id_producto=id_producto).first()
    if item:
        item.cantidad += 1
        db.session.commit()
    return redirect(url_for('main.ver_carrito'))


@main_bp.route('/carrito/restar/<int:id_producto>', methods=['POST'])
@login_required
def restar_cantidad(id_producto):
    item = Carrito.query.filter_by(id_usuario=current_user.id, id_producto=id_producto).first()
    if item:
        if item.cantidad > 1:
            item.cantidad -= 1
        else:
            db.session.delete(item)
        db.session.commit()
    return redirect(url_for('main.ver_carrito'))


@main_bp.route('/carrito/vaciar', methods=['POST'])
@login_required
def vaciar_carrito():
    Carrito.query.filter_by(id_usuario=current_user.id).delete()
    db.session.commit()
    return redirect(url_for('main.ver_carrito'))


@main_bp.route('/carrito/finalizar', methods=['POST'])
@login_required
def finalizar_compra():
    items_carrito = Carrito.query.filter_by(id_usuario=current_user.id).all()
    if not items_carrito:
        return redirect(url_for('main.catalogo'))

    total = sum(item.producto.precio * item.cantidad for item in items_carrito)
    nueva_venta = Venta(id_usuario=current_user.id, total_pago=total, estado_envio='pendiente')
    db.session.add(nueva_venta)
    db.session.flush()

    for item in items_carrito:
        detalle = DetalleVenta(
            id_venta=nueva_venta.id,
            id_producto=item.id_producto,
            cantidad=item.cantidad,
            precio_unitario=item.producto.precio
        )
        db.session.add(detalle)

    Carrito.query.filter_by(id_usuario=current_user.id).delete()
    db.session.commit()
    flash('¡Compra exitosa!', 'success')
    return redirect(url_for('main.mis_compras'))


@main_bp.route('/quiero-vender')
@login_required
def quiero_vender():
    # Si ya es vendedor, lo mandamos al catálogo o a su panel
    if current_user.rol == 'vendedor':
        flash('Ya eres un vendedor registrado.', 'info')
        return redirect(url_for('main.perfil'))
    return render_template('vender_registro.html')


@main_bp.route('/convertir-en-vendedor', methods=['POST'])
@login_required
def convertir_vendedor():
    try:
        current_user.rol = 'vendedor'
        db.session.commit()
        flash('¡Felicidades! Ahora tienes una cuenta de Vendedor.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Hubo un error al procesar tu solicitud.', 'danger')

    return redirect(url_for('main.perfil'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.rol != 'vendedor':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('main.perfil'))

    # 1. Obtenemos el ID del usuario de forma segura
    # Según tu error anterior, current_user.id_usuario no existía,
    # por lo que probablemente sea current_user.id
    user_id = current_user.id

    # 2. FILTRADO CRUCIAL:
    # Añadimos 'activo=True' para que no intente mostrar los que "borramos"
    # y usamos la columna correcta 'id_vendedor'
    mis_productos = Producto.query.filter_by(
        id_vendedor=user_id,
        activo=True
    ).all()

    return render_template('dashboard.html', productos=mis_productos)

@main_bp.route('/producto/nuevo', methods=['GET', 'POST'])
@login_required
def crear_producto():
    if current_user.rol != 'vendedor':
        flash('Debes ser vendedor para publicar productos.', 'danger')
        return redirect(url_for('main.perfil'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = request.form.get('precio')
        stock = request.form.get('stock')
        imagen_url = request.form.get('imagen_url')
        id_categoria = request.form.get('id_categoria')

        try:
            nuevo_prod = Producto(
                nombre=nombre,
                descripcion=descripcion,
                precio=float(precio),
                stock=int(stock),
                imagen_url=imagen_url,
                # Convertimos a int para que coincida con la FK de la DB
                id_categoria=int(id_categoria) if id_categoria else None,
                id_vendedor=current_user.id
            )

            db.session.add(nuevo_prod)
            db.session.commit()
            flash('¡Producto publicado con éxito!', 'success')
            return redirect(url_for('main.dashboard'))

        except Exception as e:
            db.session.rollback()
            print(f"Error detectado: {e}") # Para que lo veas en consola
            flash(f'Error al publicar: {str(e)}', 'danger')
            return redirect(url_for('main.crear_producto'))

    # IMPORTANTE: Cargamos categorías para el select
    categorias = Categoria.query.all()
    return render_template('nuevo_producto.html', categorias=categorias)


# RUTA: EDITAR PRODUCTO
@main_bp.route('/producto/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    # Usamos id_producto que es tu Primary Key
    producto = Producto.query.get_or_404(id)

    # Verificamos usando id_vendedor (el nombre en tu modelo)
    if producto.id_vendedor != current_user.id:
        flash('No tienes permiso para editar este producto.', 'danger')
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        try:
            producto.nombre = request.form.get('nombre')
            producto.precio = float(request.form.get('precio'))
            producto.stock = int(request.form.get('stock'))
            producto.descripcion = request.form.get('descripcion')

            db.session.commit()
            flash(f'¡{producto.nombre} actualizado correctamente!', 'success')
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar el producto.', 'danger')

    return render_template('editar_producto.html', producto=producto)


# RUTA: ELIMINAR PRODUCTO
@main_bp.route('/producto/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)

    # Usar el ID correcto según lo que descubrimos antes
    user_id = getattr(current_user, 'id_usuario', getattr(current_user, 'id', None))

    if producto.id_vendedor != user_id:
        flash('Acción no autorizada.', 'danger')
        return redirect(url_for('main.dashboard'))

    # BORRADO LÓGICO:
    producto.activo = False
    db.session.commit()

    flash(f'El producto "{producto.nombre}" ha sido eliminado de tu inventario.', 'warning')
    return redirect(url_for('main.dashboard'))


@main_bp.after_request
def add_header(response):
    # Estas cabeceras le dicen al navegador:
    # "No guardes una copia de esta página en el disco ni en memoria"
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response