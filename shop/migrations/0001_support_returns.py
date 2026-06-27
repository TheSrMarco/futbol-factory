from django.db import migrations


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TABLE IF NOT EXISTS public.soporte (
                id_soporte serial PRIMARY KEY,
                id_usuario integer NOT NULL REFERENCES public.usuarios(id_usuario) ON DELETE CASCADE,
                asunto character varying(120) NOT NULL,
                mensaje text NOT NULL,
                estado character varying(30) DEFAULT 'abierto'::character varying NOT NULL,
                fecha_creacion timestamp with time zone DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS public.devoluciones (
                id_devolucion serial PRIMARY KEY,
                id_venta integer NOT NULL REFERENCES public.ventas(id_venta) ON DELETE CASCADE,
                id_usuario integer NOT NULL REFERENCES public.usuarios(id_usuario) ON DELETE CASCADE,
                motivo text NOT NULL,
                estado character varying(30) DEFAULT 'solicitada'::character varying NOT NULL,
                fecha_solicitud timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT devoluciones_venta_usuario_key UNIQUE (id_venta, id_usuario)
            );
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
