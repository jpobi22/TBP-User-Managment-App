from django.db import migrations

SQL = r"""
CREATE OR REPLACE FUNCTION audit_trigger_fn()
RETURNS TRIGGER AS $$
DECLARE
    pk_value TEXT;
    changed_by_value TEXT;
BEGIN
    changed_by_value := current_setting('app.changed_by', true);

    IF (TG_OP = 'DELETE') THEN
        pk_value := COALESCE(OLD.id::text, NULL);
        INSERT INTO audit_log(table_name, action, row_pk, changed_by, old_data, new_data)
        VALUES (TG_TABLE_NAME, TG_OP, pk_value, changed_by_value, to_jsonb(OLD), NULL);
        RETURN OLD;

    ELSIF (TG_OP = 'UPDATE') THEN
        pk_value := COALESCE(NEW.id::text, NULL);
        INSERT INTO audit_log(table_name, action, row_pk, changed_by, old_data, new_data)
        VALUES (TG_TABLE_NAME, TG_OP, pk_value, changed_by_value, to_jsonb(OLD), to_jsonb(NEW));
        RETURN NEW;

    ELSIF (TG_OP = 'INSERT') THEN
        pk_value := COALESCE(NEW.id::text, NULL);
        INSERT INTO audit_log(table_name, action, row_pk, changed_by, old_data, new_data)
        VALUES (TG_TABLE_NAME, TG_OP, pk_value, changed_by_value, NULL, to_jsonb(NEW));
        RETURN NEW;
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;
"""

REVERSE_SQL = r"""
-- Reverse vraća na staru verziju bez changed_by (opcionalno),
-- ali najčešće je dovoljno samo dropati pa će idući migrate vratiti.
-- Ostavit ćemo no-op reverse da ne brišemo audit mehanizam.
"""

class Migration(migrations.Migration):

    dependencies = [
    ("accounts", "0005_pg_has_permission_function"),
]


    operations = [
        migrations.RunSQL(SQL, REVERSE_SQL),
    ]
