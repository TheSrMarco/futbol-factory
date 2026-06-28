# Futbol Factory

Aplicacion web Django para compra y venta de productos deportivos. El proyecto
usa PostgreSQL, Bootstrap y plantillas Django para centralizar catalogo,
carrito, compras, perfiles, panel de vendedor y administracion.

## Tecnologias

- Python
- Django
- PostgreSQL
- Bootstrap
- Django templates
- Django CSRF middleware

## Estado actual del proyecto

El repositorio se encuentra estructurado como una aplicacion Django. La entrada
principal es `manage.py`; el paquete `futbol_factory/` contiene la configuracion
general y la app `shop/` concentra modelos, vistas, rutas, servicios,
plantillas y controles de acceso.

La version actual incluye:

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

Tambien puedes usar el wrapper opcional:

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

## Arquitectura Django

- `manage.py` ejecuta los comandos principales de Django.
- `futbol_factory/` contiene configuracion, URLs generales, ASGI y WSGI.
- `shop/` concentra reglas de negocio, modelos, vistas, servicios, rutas y
  context processors.
- `templates/shop/` contiene las pantallas renderizadas por Django.
- `static/` contiene estilos y recursos visuales.
- `script.py` es un wrapper opcional para arrancar el servidor local.
- Los modelos Django apuntan a las tablas existentes (`usuarios`,
  `productos`, `carrito`, `ventas`, etc.) con `managed = False`.
- La verificacion de contrasenas usa Werkzeug para mantener compatibilidad con
  los hashes actuales de la base de datos.
- Los formularios usan `{% csrf_token %}` y el middleware CSRF de Django.
- El cierre de compra usa `transaction.atomic()` y valida stock/precio vigente
  antes de crear la venta.
- Los mensajes de Django se mapean a alertas Bootstrap y las acciones sensibles
  piden confirmacion en el navegador.

## Pendientes productivos

- Integrar pasarela de pago real con tokenizacion.
- Agregar CAPTCHA y 2FA si el sistema se publica fuera del entorno academico.
- Desplegar con HTTPS, HSTS y cookies seguras.
- Agregar pruebas automatizadas para login, catalogo, carrito, compra y roles.
- Sustituir datos personales del `database.sql` por datos de prueba anonimos si
  el repositorio se mantiene publico.

## Flujo Git recomendado

Antes de publicar cambios, verifica el proyecto y crea un commit claro:

```powershell
python manage.py check
git status
git add .
git commit -m "chore: describir cambio"
git push
```
