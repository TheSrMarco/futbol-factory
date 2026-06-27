from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('login/', views.login_view, name='login'),
    path('auth/', views.auth_redirect, name='auth_legacy'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('mis-compras/', views.mis_compras, name='mis_compras'),
    path('soporte/', views.soporte, name='soporte'),
    path('mis-compras/<int:id_venta>/devolucion/', views.solicitar_devolucion, name='solicitar_devolucion'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:id_producto>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/sumar/<int:id_producto>/', views.sumar_cantidad, name='sumar_cantidad'),
    path('carrito/restar/<int:id_producto>/', views.restar_cantidad, name='restar_cantidad'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('carrito/finalizar/', views.finalizar_compra, name='finalizar_compra'),
    path('quiero-vender/', views.quiero_vender, name='quiero_vender'),
    path('convertir-en-vendedor/', views.convertir_vendedor, name='convertir_vendedor'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('producto/nuevo/', views.crear_producto, name='crear_producto'),
    path('producto/editar/<int:id_producto>/', views.editar_producto, name='editar_producto'),
    path('producto/eliminar/<int:id_producto>/', views.eliminar_producto, name='eliminar_producto'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/usuarios/<int:id_usuario>/rol/', views.admin_cambiar_rol, name='admin_cambiar_rol'),
    path('admin-panel/productos/<int:id_producto>/estado/', views.admin_toggle_producto, name='admin_toggle_producto'),
    path('admin-panel/soporte/<int:id_soporte>/estado/', views.admin_actualizar_soporte, name='admin_actualizar_soporte'),
    path('admin-panel/devoluciones/<int:id_devolucion>/estado/', views.admin_actualizar_devolucion, name='admin_actualizar_devolucion'),
]
