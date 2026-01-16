from django.db import migrations

SQL = r"""
-- 1) Audit tablica
CREATE TABLE IF NOT EXISTS audit_log (
    id BIGSERIAL PRIMARY KEY,
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    table_name TEXT NOT NULL,
    action TEXT NOT NULL, -- INSERT/UPDATE/DELETE
    row_pk TEXT NULL,
    changed_by TEXT NULL, -- možemo kasnije povezati s app logikom (request user)
    old_data JSONB NULL,
    new_data JSONB NULL
);

"""




REVERSE_SQL = r"""
DROP VIEW IF EXISTS v_user_effective_permissions;
DROP FUNCTION IF EXISTS has_permission(INT, TEXT, TEXT);
DROP TRIGGER IF EXISTS tr_audit_auth_user ON auth_user;
DROP TRIGGER IF EXISTS tr_audit_accounts_userprofile ON accounts_userprofile;
DROP FUNCTION IF EXISTS audit_trigger_fn();
DROP TABLE IF EXISTS audit_log;
"""


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(SQL, REVERSE_SQL),
    ]
