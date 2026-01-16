from django.db import migrations

SQL = r"""
CREATE OR REPLACE VIEW v_user_effective_permissions AS
SELECT
    u.id AS user_id,
    u.username,
    p.id AS permission_id,
    p.codename,
    ct.app_label
FROM auth_user u
JOIN auth_user_user_permissions uup ON uup.user_id = u.id
JOIN auth_permission p ON p.id = uup.permission_id
JOIN django_content_type ct ON ct.id = p.content_type_id

UNION

SELECT
    u.id AS user_id,
    u.username,
    p.id AS permission_id,
    p.codename,
    ct.app_label
FROM auth_user u
JOIN auth_user_groups ug ON ug.user_id = u.id
JOIN auth_group_permissions gp ON gp.group_id = ug.group_id
JOIN auth_permission p ON p.id = gp.permission_id
JOIN django_content_type ct ON ct.id = p.content_type_id;
"""

REVERSE_SQL = r"""
DROP VIEW IF EXISTS v_user_effective_permissions;
"""

class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_pg_audit_triggers"),
    ]

    operations = [
        migrations.RunSQL(SQL, REVERSE_SQL),
    ]
