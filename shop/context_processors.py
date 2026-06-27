from .services import get_current_usuario


def current_usuario(request):
    return {'current_usuario': get_current_usuario(request)}
