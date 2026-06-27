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
]
