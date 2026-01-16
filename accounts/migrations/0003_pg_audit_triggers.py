from django.db import migrations

SQL = r"""
-- Trigger funkcija za audit
CREATE OR REPLACE FUNCTION audit_trigger_fn()
RETURNS TRIGGER AS $$
DECLARE
    pk_value TEXT;
BEGIN
    IF (TG_OP = 'DELETE') THEN
        pk_value := COALESCE(OLD.id::text, NULL);
        INSERT INTO audit_log(table_name, action, row_pk, old_data, new_data)
        VALUES (TG_TABLE_NAME, TG_OP, pk_value, to_jsonb(OLD), NULL);
        RETURN OLD;

    ELSIF (TG_OP = 'UPDATE') THEN
        pk_value := COALESCE(NEW.id::text, NULL);
        INSERT INTO audit_log(table_name, action, row_pk, old_data, new_data)
        VALUES (TG_TABLE_NAME, TG_OP, pk_value, to_jsonb(OLD), to_jsonb(NEW));
        RETURN NEW;

    ELSIF (TG_OP = 'INSERT') THEN
        pk_value := COALESCE(NEW.id::text, NULL);
        INSERT INTO audit_log(table_name, action, row_pk, old_data, new_data)
        VALUES (TG_TABLE_NAME, TG_OP, pk_value, NULL, to_jsonb(NEW));
        RETURN NEW;
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Triggeri (kreiraj samo ako ne postoje)
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'auth_user') THEN
        IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'tr_audit_auth_user') THEN
            CREATE TRIGGER tr_audit_auth_user
            AFTER INSERT OR UPDATE OR DELETE ON auth_user
            FOR EACH ROW EXECUTE FUNCTION audit_trigger_fn();
        END IF;
    END IF;

    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'accounts_userprofile') THEN
        IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'tr_audit_accounts_userprofile') THEN
            CREATE TRIGGER tr_audit_accounts_userprofile
            AFTER INSERT OR UPDATE OR DELETE ON accounts_userprofile
            FOR EACH ROW EXECUTE FUNCTION audit_trigger_fn();
        END IF;
    END IF;
END $$;
"""

REVERSE_SQL = r"""
DROP TRIGGER IF EXISTS tr_audit_auth_user ON auth_user;
DROP TRIGGER IF EXISTS tr_audit_accounts_userprofile ON accounts_userprofile;
DROP FUNCTION IF EXISTS audit_trigger_fn();
"""

class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_pg_audit_and_permissions"),
    ]

    operations = [
        migrations.RunSQL(SQL, REVERSE_SQL),
    ]
