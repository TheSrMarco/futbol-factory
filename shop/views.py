from decimal import Decimal
from urllib.parse import urlsplit

from django.contrib import messages
from django.db import transaction
from django.db.models import F, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from werkzeug.security import check_password_hash, generate_password_hash

from .models import Carrito, Categoria, DetalleVenta, Producto, Usuario, Venta
from .services import SESSION_USER_KEY, admin_required, get_current_usuario, login_required_view, vendedor_required


ROLES = {'admin', 'cliente', 'vendedor'}


def _safe_next_url(request):
    next_url = request.GET.get('next')
    if next_url and next_url.startswith('/') and not urlsplit(next_url).netloc:
        return next_url
    return '/'


def home(request):
    productos = Producto.objects.filter(activo=True).select_related('categoria').order_by('-id_producto')[:3]
    return render(request, 'shop/index.html', {'productos': productos})


def catalogo(request):
    categoria_id = request.GET.get('cat')
    productos = Producto.objects.filter(activo=True).select_related('categoria')
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    return render(
        request,
        'shop/catalogo.html',
        {
            'productos': productos,
            'categorias': Categoria.objects.all().order_by('nombre'),
            'categoria_actual': int(categoria_id) if categoria_id and categoria_id.isdigit() else None,
        },
    )


def login_view(request):
    if get_current_usuario(request):
        return redirect('home')

    if request.method == 'GET':
        return render(request, 'shop/login.html')

    email = (request.POST.get('email') or '').strip().lower()
    password = request.POST.get('password') or ''

    if not email or not password:
        messages.error(request, 'Correo y contrasena son obligatorios.')
        return redirect('login')

    usuario = Usuario.objects.filter(email=email).first()
    if not usuario or not check_password_hash(usuario.password, password):
        messages.error(request, 'Correo o contrasena incorrectos.')
        return redirect('login')

    request.session.cycle_key()
    request.session[SESSION_USER_KEY] = usuario.id_usuario
    return redirect(_safe_next_url(request))


def auth_redirect(request):
    return redirect('login')


def registro(request):
    if request.method != 'POST':
        return redirect('login')

    nombre = (request.POST.get('nombre') or '').strip()
    email = (request.POST.get('email') or '').strip().lower()
    password = request.POST.get('password') or ''

    if not nombre or not email or not password:
        messages.error(request, 'Completa todos los campos obligatorios.')
        return redirect('login')

    if len(password) < 8:
        messages.error(request, 'La contrasena debe tener al menos 8 caracteres.')
        return redirect('login')

    if Usuario.objects.filter(email=email).exists():
        messages.warning(request, 'Ese correo ya esta registrado.')
        return redirect('login')

    Usuario.objects.create(
        nombre=nombre,
        email=email,
        password=generate_password_hash(password, method='pbkdf2:sha256'),
        rol='cliente',
    )
    messages.success(request, 'Cuenta creada correctamente. Ahora inicia sesion.')
    return redirect('login')


def logout_view(request):
    request.session.flush()
    messages.info(request, 'Has cerrado sesion correctamente.')
    return redirect('login')


@login_required_view
def perfil(request):
    return render(request, 'shop/perfil.html')


@login_required_view
def mis_compras(request):
    usuario = get_current_usuario(request)
    compras = Venta.objects.filter(usuario=usuario).prefetch_related('detalles__producto').order_by('-fecha')
    return render(request, 'shop/mis_compras.html', {'compras': compras})


@login_required_view
def agregar_al_carrito(request, id_producto):
    if request.method != 'POST':
        return redirect('catalogo')

    usuario = get_current_usuario(request)
    producto = get_object_or_404(Producto, pk=id_producto, activo=True)
    if producto.stock < 1:
        messages.warning(request, 'Este producto no tiene stock disponible.')
        return redirect('catalogo')

    item, created = Carrito.objects.get_or_create(
        usuario=usuario,
        producto=producto,
        defaults={'cantidad': 1},
    )
    if not created:
        if item.cantidad >= producto.stock:
            messages.warning(request, 'No hay mas stock disponible para este producto.')
            return redirect('ver_carrito')
        item.cantidad = F('cantidad') + 1
        item.save(update_fields=['cantidad'])

    messages.success(request, 'Producto agregado al carrito.')
    return redirect('catalogo')


@login_required_view
def ver_carrito(request):
    usuario = get_current_usuario(request)
    items = Carrito.objects.filter(usuario=usuario).select_related('producto').order_by('id_carrito')
    total = sum(item.producto.precio * item.cantidad for item in items)
    return render(request, 'shop/carrito.html', {'items': items, 'total': total})


@login_required_view
def sumar_cantidad(request, id_producto):
    if request.method == 'POST':
        usuario = get_current_usuario(request)
        item = Carrito.objects.select_related('producto').filter(usuario=usuario, producto_id=id_producto).first()
        if item and item.cantidad < item.producto.stock:
            item.cantidad += 1
            item.save(update_fields=['cantidad'])
        elif item:
            messages.warning(request, 'No hay mas stock disponible.')
    return redirect('ver_carrito')


@login_required_view
def restar_cantidad(request, id_producto):
    if request.method == 'POST':
        usuario = get_current_usuario(request)
        item = Carrito.objects.filter(usuario=usuario, producto_id=id_producto).first()
        if item:
            if item.cantidad > 1:
                item.cantidad -= 1
                item.save(update_fields=['cantidad'])
            else:
                item.delete()
    return redirect('ver_carrito')


@login_required_view
def vaciar_carrito(request):
    if request.method == 'POST':
        Carrito.objects.filter(usuario=get_current_usuario(request)).delete()
    return redirect('ver_carrito')


@login_required_view
def finalizar_compra(request):
    if request.method != 'POST':
        return redirect('ver_carrito')

    usuario = get_current_usuario(request)
    with transaction.atomic():
        items = list(Carrito.objects.select_related('producto').filter(usuario=usuario).order_by('id_carrito'))
        if not items:
            messages.info(request, 'Tu carrito esta vacio.')
            return redirect('catalogo')

        productos = {
            producto.id_producto: producto
            for producto in Producto.objects.select_for_update().filter(
                id_producto__in=[item.producto_id for item in items],
                activo=True,
            )
        }

        total = Decimal('0.00')
        for item in items:
            producto = productos.get(item.producto_id)
            if not producto:
                messages.error(request, 'Un producto del carrito ya no esta disponible.')
                return redirect('ver_carrito')
            if item.cantidad > producto.stock:
                messages.error(request, f'Stock insuficiente para {producto.nombre}.')
                return redirect('ver_carrito')
            total += producto.precio * item.cantidad

        venta = Venta.objects.create(
            usuario=usuario,
            fecha=timezone.now(),
            total_pago=total,
            estado_envio='pendiente',
        )

        for item in items:
            producto = productos[item.producto_id]
            DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=item.cantidad,
                precio_unitario=producto.precio,
            )
            producto.stock -= item.cantidad
            producto.save(update_fields=['stock'])

        Carrito.objects.filter(usuario=usuario).delete()

    messages.success(request, 'Compra exitosa.')
    return redirect('mis_compras')


@login_required_view
def quiero_vender(request):
    usuario = get_current_usuario(request)
    if usuario.rol == 'admin':
        messages.info(request, 'Tu cuenta ya tiene permisos de administrador.')
        return redirect('admin_dashboard')
    if usuario.rol == 'vendedor':
        messages.info(request, 'Ya eres vendedor.')
        return redirect('perfil')
    return render(request, 'shop/vender_registro.html')


@login_required_view
def convertir_vendedor(request):
    if request.method == 'POST':
        usuario = get_current_usuario(request)
        usuario.rol = 'vendedor'
        usuario.save(update_fields=['rol'])
        messages.success(request, 'Ahora tienes una cuenta de vendedor.')
    return redirect('perfil')


@vendedor_required
def dashboard(request):
    usuario = get_current_usuario(request)
    productos = Producto.objects.filter(vendedor=usuario, activo=True).select_related('categoria')
    stock_bajo = productos.filter(stock__lte=2).count()
    return render(request, 'shop/dashboard.html', {'productos': productos, 'stock_bajo': stock_bajo})


@vendedor_required
def crear_producto(request):
    if request.method == 'POST':
        return _guardar_producto(request)

    return render(
        request,
        'shop/producto_form.html',
        {'categorias': Categoria.objects.all().order_by('nombre'), 'producto': None},
    )


@vendedor_required
def editar_producto(request, id_producto):
    producto = get_object_or_404(Producto, pk=id_producto, vendedor=get_current_usuario(request), activo=True)
    if request.method == 'POST':
        return _guardar_producto(request, producto)

    return render(
        request,
        'shop/producto_form.html',
        {'categorias': Categoria.objects.all().order_by('nombre'), 'producto': producto},
    )


def _guardar_producto(request, producto=None):
    usuario = get_current_usuario(request)
    nombre = (request.POST.get('nombre') or '').strip()
    descripcion = (request.POST.get('descripcion') or '').strip()
    imagen_url = (request.POST.get('imagen_url') or '').strip()
    categoria_id = request.POST.get('id_categoria') or None

    try:
        precio = Decimal(request.POST.get('precio') or '0')
        stock = int(request.POST.get('stock') or '0')
    except Exception:
        messages.error(request, 'Precio o stock invalido.')
        return _redirect_producto_form(producto)

    if not nombre or precio < 0 or stock < 0:
        messages.error(request, 'Completa los datos del producto correctamente.')
        return _redirect_producto_form(producto)

    if producto is None:
        producto = Producto(vendedor=usuario)

    producto.nombre = nombre
    producto.descripcion = descripcion
    producto.precio = precio
    producto.stock = stock
    producto.imagen_url = imagen_url
    producto.categoria_id = categoria_id
    producto.activo = True
    producto.save()

    messages.success(request, 'Producto guardado correctamente.')
    return redirect('dashboard')


def _redirect_producto_form(producto):
    if producto is None:
        return redirect('crear_producto')
    return redirect('editar_producto', id_producto=producto.id_producto)


@vendedor_required
def eliminar_producto(request, id_producto):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, pk=id_producto, vendedor=get_current_usuario(request))
        producto.activo = False
        producto.save(update_fields=['activo'])
        messages.warning(request, 'Producto eliminado del inventario.')
    return redirect('dashboard')


@admin_required
def admin_dashboard(request):
    usuarios = Usuario.objects.all().order_by('id_usuario')
    productos = Producto.objects.select_related('categoria', 'vendedor').order_by('-id_producto')
    ventas = Venta.objects.select_related('usuario').prefetch_related('detalles__producto').order_by('-fecha')
    total_ventas = ventas.aggregate(total=Sum('total_pago'))['total'] or Decimal('0.00')

    stats = {
        'usuarios': usuarios.count(),
        'clientes': usuarios.filter(rol='cliente').count(),
        'vendedores': usuarios.filter(rol='vendedor').count(),
        'admins': usuarios.filter(rol='admin').count(),
        'productos_activos': productos.filter(activo=True).count(),
        'ventas': ventas.count(),
        'total_ventas': total_ventas,
    }

    return render(
        request,
        'shop/admin_dashboard.html',
        {
            'usuarios': usuarios,
            'productos': productos[:20],
            'ventas': ventas[:10],
            'stats': stats,
            'roles': sorted(ROLES),
        },
    )


@admin_required
def admin_cambiar_rol(request, id_usuario):
    if request.method != 'POST':
        return redirect('admin_dashboard')

    usuario = get_object_or_404(Usuario, pk=id_usuario)
    nuevo_rol = request.POST.get('rol')
    if nuevo_rol not in ROLES:
        messages.error(request, 'Rol invalido.')
        return redirect('admin_dashboard')

    if usuario.id_usuario == get_current_usuario(request).id_usuario and nuevo_rol != 'admin':
        messages.warning(request, 'No puedes quitarte el rol admin desde tu propia sesion.')
        return redirect('admin_dashboard')

    usuario.rol = nuevo_rol
    usuario.save(update_fields=['rol'])
    messages.success(request, f'Rol actualizado para {usuario.email}.')
    return redirect('admin_dashboard')


@admin_required
def admin_toggle_producto(request, id_producto):
    if request.method != 'POST':
        return redirect('admin_dashboard')

    producto = get_object_or_404(Producto, pk=id_producto)
    producto.activo = not producto.activo
    producto.save(update_fields=['activo'])
    estado = 'activado' if producto.activo else 'desactivado'
    messages.info(request, f'Producto {estado}: {producto.nombre}.')
    return redirect('admin_dashboard')
