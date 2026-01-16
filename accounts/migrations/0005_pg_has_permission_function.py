from django.db import migrations

SQL = r"""
CREATE OR REPLACE FUNCTION has_permission(p_user_id INT, p_app_label TEXT, p_codename TEXT)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1
        FROM v_user_effective_permissions v
        WHERE v.user_id = p_user_id
          AND v.app_label = p_app_label
          AND v.codename = p_codename
    );
END;
$$ LANGUAGE plpgsql STABLE;
"""

REVERSE_SQL = r"""
DROP FUNCTION IF EXISTS has_permission(INT, TEXT, TEXT);
"""

class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_pg_effective_permissions_view"),
    ]

    operations = [
        migrations.RunSQL(SQL, REVERSE_SQL),
    ]
