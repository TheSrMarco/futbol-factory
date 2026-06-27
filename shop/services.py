from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from .models import Usuario


SESSION_USER_KEY = 'usuario_id'


def get_current_usuario(request):
    usuario_id = request.session.get(SESSION_USER_KEY)
    if not usuario_id:
        return None

    if getattr(request, '_cached_usuario', None) is not None:
        return request._cached_usuario

    try:
        request._cached_usuario = Usuario.objects.get(pk=usuario_id)
    except Usuario.DoesNotExist:
        request.session.pop(SESSION_USER_KEY, None)
        request._cached_usuario = None

    return request._cached_usuario


def login_required_view(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        if not get_current_usuario(request):
            return redirect(f'/login/?next={request.path}')
        return view_func(request, *args, **kwargs)

    return wrapped


def vendedor_required(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        usuario = get_current_usuario(request)
        if not usuario:
            return redirect(f'/login/?next={request.path}')
        if usuario.rol != 'vendedor':
            messages.error(request, 'Acceso denegado.')
            return redirect('perfil')
        return view_func(request, *args, **kwargs)

    return wrapped


def admin_required(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        usuario = get_current_usuario(request)
        if not usuario:
            return redirect(f'/login/?next={request.path}')
        if usuario.rol != 'admin':
            messages.error(request, 'Acceso reservado para administradores.')
            return redirect('perfil')
        return view_func(request, *args, **kwargs)

    return wrapped
