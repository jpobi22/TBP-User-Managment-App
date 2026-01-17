from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import UserProfile
import random


class Command(BaseCommand):
    help = "Seed demo data for Carlsberg Koprivnica user management."

    def handle(self, *args, **options):

       
        groups = {
            "IT_ADMIN": "Puni pristup upravljanju korisnicima i sustavom",
            "HR_MANAGER": "Upravljanje metapodacima i osnovnim korisničkim podacima",
            "READ_ONLY": "Samo čitanje (audit i pregled)",
        }

        group_objs = {}
        for gname in groups.keys():
            g, _ = Group.objects.get_or_create(name=gname)
            group_objs[gname] = g

        user_ct = ContentType.objects.get(app_label="auth", model="user")
        profile_ct = ContentType.objects.get(app_label="accounts", model="userprofile")

        user_perms = Permission.objects.filter(content_type=user_ct)
        profile_perms = Permission.objects.filter(content_type=profile_ct)

        portal_perms = Permission.objects.filter(
            content_type=profile_ct,
            codename__in=[
                "access_it_portal",
                "access_hr_portal",
                "access_sales_portal",
                "access_audit_portal",
            ],
        )

        group_objs["IT_ADMIN"].permissions.set(list(user_perms) + list(profile_perms) + list(portal_perms))

        hr_perms = []
        for codename in ["view_user", "change_user"]:
            p = Permission.objects.filter(content_type=user_ct, codename=codename).first()
            if p:
                hr_perms.append(p)

        for codename in ["view_userprofile", "change_userprofile"]:
            p = Permission.objects.filter(content_type=profile_ct, codename=codename).first()
            if p:
                hr_perms.append(p)

        p_hr_portal = Permission.objects.filter(content_type=profile_ct, codename="access_hr_portal").first()
        if p_hr_portal:
            hr_perms.append(p_hr_portal)

        group_objs["HR_MANAGER"].permissions.set(hr_perms)

        ro_perms = []
        for codename in ["view_user"]:
            p = Permission.objects.filter(content_type=user_ct, codename=codename).first()
            if p:
                ro_perms.append(p)

        for codename in ["view_userprofile"]:
            p = Permission.objects.filter(content_type=profile_ct, codename=codename).first()
            if p:
                ro_perms.append(p)

        p_audit_portal = Permission.objects.filter(content_type=profile_ct, codename="access_audit_portal").first()
        if p_audit_portal:
            ro_perms.append(p_audit_portal)

        group_objs["READ_ONLY"].permissions.set(ro_perms)

       
        demo_users = [
            
            ("itguy", "itguy@carlsberg.local", "IT_ADMIN", "IT", "System Admin"),
            ("itadmin", "itadmin@carlsberg.local", "IT_ADMIN", "IT", "IT Manager"),
            ("itsupport", "itsupport@carlsberg.local", "READ_ONLY", "IT", "IT Support"),

            
            ("hrmaria", "hrmaria@carlsberg.local", "HR_MANAGER", "HR", "HR Manager"),
            ("hrana", "hrana@carlsberg.local", "READ_ONLY", "HR", "HR Specialist"),

            
            ("salesivan", "salesivan@carlsberg.local", "READ_ONLY", "Sales", "Sales Rep"),
            ("salespetra", "salespetra@carlsberg.local", "READ_ONLY", "Sales", "Key Account Manager"),

            
            ("shiftlead", "shiftlead@carlsberg.local", "READ_ONLY", "Production", "Shift Lead"),
            ("operatorluka", "operatorluka@carlsberg.local", "READ_ONLY", "Production", "Operator"),

            
            ("warehousemarko", "warehousemarko@carlsberg.local", "READ_ONLY", "Logistics", "Warehouse Coordinator"),
        ]

        created_count = 0

        for username, email, role, dept, title in demo_users:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"email": email, "is_staff": False},
            )
            if created:
                user.set_password("Carlsberg123!")
                user.save()
                created_count += 1

            user.groups.set([group_objs[role]])

            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.department = dept
            profile.job_title = title
            profile.is_active_employee = True
            profile.metadata = {
                "company": "Carlsberg Koprivnica",
                "site": "Koprivnica",
                "badge_id": f"CK-{random.randint(10000, 99999)}",
                "shift": random.choice(["A", "B", "C"]),
                "created_for_demo": True,
            }
            profile.save()

        self.stdout.write(self.style.SUCCESS(f"Seed completed. New users created: {created_count}"))
        self.stdout.write(self.style.WARNING("Demo password for seeded users: Carlsberg123!"))
