from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0001_support_returns'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TABLE IF NOT EXISTS public.solicitudes_vendedor (
                id_solicitud serial PRIMARY KEY,
                id_usuario integer NOT NULL REFERENCES public.usuarios(id_usuario) ON DELETE CASCADE,
                mensaje text,
                estado character varying(30) DEFAULT 'pendiente'::character varying NOT NULL,
                fecha_solicitud timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT solicitudes_vendedor_usuario_key UNIQUE (id_usuario)
            );
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
