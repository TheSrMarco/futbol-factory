from django.db import models


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    rol = models.CharField(max_length=20, default='cliente')
    nombre = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios'

    def __str__(self):
        return self.email


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'categorias'

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.IntegerField(default=0)
    imagen_url = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    categoria = models.ForeignKey(
        Categoria,
        models.SET_NULL,
        db_column='id_categoria',
        blank=True,
        null=True,
        related_name='productos',
    )
    vendedor = models.ForeignKey(
        Usuario,
        models.CASCADE,
        db_column='id_vendedor',
        blank=True,
        null=True,
        related_name='productos',
    )

    class Meta:
        managed = False
        db_table = 'productos'

    def __str__(self):
        return self.nombre


class Carrito(models.Model):
    id_carrito = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        Usuario,
        models.CASCADE,
        db_column='id_usuario',
        related_name='items_carrito',
    )
    producto = models.ForeignKey(
        Producto,
        models.CASCADE,
        db_column='id_producto',
        related_name='items_carrito',
    )
    cantidad = models.IntegerField(default=1)

    class Meta:
        managed = False
        db_table = 'carrito'


class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        Usuario,
        models.DO_NOTHING,
        db_column='id_usuario',
        related_name='ventas',
    )
    fecha = models.DateTimeField(blank=True, null=True)
    total_pago = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado_envio = models.CharField(max_length=50, default='pendiente')

    class Meta:
        managed = False
        db_table = 'ventas'


class Pago(models.Model):
    id_pago = models.AutoField(primary_key=True)
    venta = models.ForeignKey(
        Venta,
        models.CASCADE,
        db_column='id_venta',
        related_name='pagos',
    )
    metodo_pago = models.CharField(max_length=50, blank=True, null=True)
    estado_pago = models.CharField(max_length=50, blank=True, null=True)
    fecha_pago = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pago'


class Sesion(models.Model):
    id_sesion = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        Usuario,
        models.CASCADE,
        db_column='id_usuario',
        related_name='sesiones',
    )
    fecha_login = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sesiones'


class Soporte(models.Model):
    id_soporte = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        Usuario,
        models.CASCADE,
        db_column='id_usuario',
        related_name='tickets_soporte',
    )
    asunto = models.CharField(max_length=120)
    mensaje = models.TextField()
    estado = models.CharField(max_length=30, default='abierto')
    fecha_creacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'soporte'


class Devolucion(models.Model):
    id_devolucion = models.AutoField(primary_key=True)
    venta = models.ForeignKey(
        Venta,
        models.CASCADE,
        db_column='id_venta',
        related_name='devoluciones',
    )
    usuario = models.ForeignKey(
        Usuario,
        models.CASCADE,
        db_column='id_usuario',
        related_name='devoluciones',
    )
    motivo = models.TextField()
    estado = models.CharField(max_length=30, default='solicitada')
    fecha_solicitud = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'devoluciones'


class DetalleVenta(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    venta = models.ForeignKey(
        Venta,
        models.CASCADE,
        db_column='id_venta',
        related_name='detalles',
    )
    producto = models.ForeignKey(
        Producto,
        models.DO_NOTHING,
        db_column='id_producto',
        related_name='detalles_venta',
    )
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'detalle_venta'
