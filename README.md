# Futbol Factory

Aplicacion web para compra y venta de productos deportivos. La documentacion del
proyecto plantea una solucion con Django, PostgreSQL y Bootstrap; por eso esta
reestructuracion deja a Django como tecnologia principal de ejecucion.

> Nota historica: el prototipo anterior estaba hecho con Flask. Ese codigo se
> conserva temporalmente en `app/` como referencia, pero la entrada correcta del
> proyecto ahora es Django mediante `manage.py`.

## Tecnologias

- Python
- Django
- PostgreSQL
- Bootstrap
- Django templates
- Django CSRF middleware

## Estado actual del proyecto

El codigo inicial encontrado en este repositorio estaba implementado con Flask,
aunque la documentacion academica describia Django, PostgreSQL y Bootstrap. Para
mantener coherencia con la documentacion S-SDLC, el proyecto fue reestructurado
a Django.

La version actual conserva:

- PostgreSQL como base de datos.
- Bootstrap para la interfaz visual.
- Templates renderizados desde servidor.
- Catalogo, login/registro, carrito, compras, perfil, dashboard de vendedor y
  panel administrador con usuarios, roles, categorias, productos, ventas, pagos
  devoluciones, soporte y accesos.
- CSRF en formularios mediante middleware de Django.
- Bloqueo temporal tras varios intentos fallidos de inicio de sesion.

Quedan como pendientes productivos los controles avanzados documentados para una
version final: pasarela de pago tokenizada, CAPTCHA, 2FA y despliegue HTTPS.

## Documentacion S-SDLC

Las entregas academicas del proyecto se encuentran en [`docs/`](docs/):

- Etapa 1: planeacion.
- Etapa 2: analisis.
- Etapa 3: diseno.
- Etapa 4: desarrollo e implementacion.

## Como se ejecuta

No abras los archivos HTML con doble clic. El proyecto es una aplicacion web de
servidor: primero se arranca Django y despues se entra desde el navegador.

1. Crea y activa un entorno virtual.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instala dependencias.

```powershell
pip install -r requirements.txt
```

3. Copia la configuracion local.

```powershell
Copy-Item .env.example .env
```

4. Edita `.env` con tu usuario y contrasena de PostgreSQL.

5. Crea la base de datos si no existe.

```sql
CREATE DATABASE ffactory;
```

6. Importa la base incluida.

```powershell
psql -U postgres -d ffactory -f database.sql
```

7. Aplica las migraciones de Django.

```powershell
python manage.py migrate
```

Este paso crea tablas internas como las usadas para registrar migraciones y
sesiones, ademas de las extensiones Django para soporte y devoluciones. Las
tablas principales del proyecto (`usuarios`, `productos`, `carrito`, `ventas`,
etc.) vienen del archivo `database.sql`.

8. Verifica que PostgreSQL este encendido.

En Windows puedes revisarlo desde `services.msc`. El servicio suele llamarse
`postgresql-x64-18` o parecido. Si tienes permisos de administrador tambien
puedes usar:

```powershell
Start-Service -Name postgresql-x64-18
```

9. Verifica la configuracion.

```powershell
python manage.py check
```

10. Arranca Django.

```powershell
python manage.py runserver
```

Tambien puedes usar el wrapper de compatibilidad:

```powershell
python script.py
```

11. Abre la aplicacion.

```text
http://127.0.0.1:8000/login/
```

Si el navegador muestra `ERR_CONNECTION_REFUSED`, Django no esta corriendo. Si
la terminal muestra `connection refused` a `localhost:5432`, PostgreSQL esta
apagado o las credenciales de `.env` no coinciden.

## Rutas principales

- `/` inicio
- `/login/` inicio de sesion y registro
- `/catalogo/` catalogo de productos
- `/carrito/` carrito de compras
- `/mis-compras/` historial de compras
- `/mis-compras/<id>/devolucion/` solicitud de devolucion
- `/perfil/` perfil de usuario
- `/soporte/` tickets de soporte
- `/dashboard/` panel de vendedor
- `/admin-panel/` panel administrador

## Roles y credenciales de prueba

El prototipo maneja tres roles principales:

- `cliente`: compra productos, administra carrito y consulta historial.
- `vendedor`: mantiene las funciones de cliente y administra su inventario.
- `admin`: revisa usuarios, cambia roles, consulta categorias, productos,
  ventas, pagos basicos, devoluciones, soporte y auditoria de accesos.

Credenciales de prueba:

```text
Admin:    yoshi@gmail.com      / root
Admin 2:  admin@ffactory.com  / root
Cliente:  cliente@ffactory.com / root
Vendedor: vendedor@ffactory.com / root
```

## Variables de entorno

- `SECRET_KEY`: clave de seguridad de Django.
- `DJANGO_DEBUG`: `true` para desarrollo local.
- `ALLOWED_HOSTS`: hosts permitidos, por ejemplo `127.0.0.1,localhost`.
- `DB_USER`: usuario de PostgreSQL.
- `DB_PASSWORD`: contrasena de PostgreSQL.
- `DB_HOST`: host de PostgreSQL.
- `DB_PORT`: puerto de PostgreSQL.
- `DB_NAME`: nombre de la base de datos.
- `DATABASE_URL`: alternativa unica para configurar PostgreSQL en despliegues.
- `DB_CONN_MAX_AGE`: segundos para reutilizar conexiones a base de datos.
- `SESSION_COOKIE_SECURE`: `true` solo con HTTPS.
- `SESSION_COOKIE_SAMESITE`: politica SameSite de cookies.
- `CSRF_COOKIE_SECURE`: `true` solo con HTTPS.
- `CSRF_COOKIE_SAMESITE`: politica SameSite del token CSRF.
- `LOGIN_ATTEMPT_LIMIT`: intentos fallidos permitidos antes del bloqueo temporal.
- `LOGIN_LOCK_SECONDS`: duracion del bloqueo temporal de login.
- `SECURE_SSL_REDIRECT`: redireccion forzada a HTTPS para despliegue.
- `SECURE_HSTS_SECONDS`: tiempo HSTS cuando el sitio ya corre sobre HTTPS.

## Decisiones de migracion

- Se agrego `manage.py` y el proyecto `futbol_factory/`.
- Se agrego el app Django `shop/`.
- El directorio `app/` se conserva como referencia del prototipo Flask original;
  la aplicacion activa para ejecucion y entrega es Django.
- Los modelos Django apuntan a las tablas existentes (`usuarios`,
  `productos`, `carrito`, `ventas`, etc.) con `managed = False`.
- Se conserva la verificacion de contrasenas existentes con Werkzeug para no
  perder compatibilidad con los hashes actuales de la base.
- Los formularios Django usan `{% csrf_token %}` y el middleware CSRF.
- El cierre de compra ahora usa `transaction.atomic()` y valida stock/precio
  vigente antes de crear la venta.
- Los mensajes de Django se mapean a alertas Bootstrap y las acciones sensibles
  piden confirmacion en el navegador.

## Buenas practicas pendientes

- Mover o eliminar el prototipo Flask de `app/` cuando Django quede aprobado.
- Eliminar HTML duplicados de la raiz antes de empaquetar.
- Limpiar `__pycache__` del entregable.
- Sustituir datos personales del `database.sql` por datos de prueba anonimos.

## Flujo Git recomendado

Trabaja los cambios en una rama separada:

```powershell
git switch -c refactor/migracion-django
```

Cuando el proyecto arranque y pase la verificacion:

```powershell
python manage.py check
git add .
git commit -m "refactor: migrar prototipo a django"
```

Para publicar la rama:

```powershell
git push -u origin refactor/migracion-django
```
