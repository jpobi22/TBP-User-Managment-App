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
        user_perms = Permission.objects.filter(content_type=user_ct)

      
        profile_ct = ContentType.objects.get(app_label="accounts", model="userprofile")
        profile_perms = Permission.objects.filter(content_type=profile_ct)


        group_objs["IT_ADMIN"].permissions.set(list(user_perms) + list(profile_perms))

        
        hr_perms = []
        for codename in ["view_user", "change_user"]:
            p = Permission.objects.filter(content_type=user_ct, codename=codename).first()
            if p:
                hr_perms.append(p)

        for codename in ["view_userprofile", "change_userprofile"]:
            p = Permission.objects.filter(content_type=profile_ct, codename=codename).first()
            if p:
                hr_perms.append(p)

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
        group_objs["READ_ONLY"].permissions.set(ro_perms)

       
        departments = ["IT", "HR", "Sales", "Production", "Logistics"]
        titles = {
            "IT": ["IT Support", "System Admin", "IT Manager"],
            "HR": ["HR Specialist", "HR Manager"],
            "Sales": ["Sales Rep", "Key Account Manager"],
            "Production": ["Shift Lead", "Operator"],
            "Logistics": ["Warehouse Coordinator", "Dispatcher"],
        }

        demo_users = [
            ("it.admin", "it.admin@carlsberg.local", "IT_ADMIN", "IT"),
            ("hr.maria", "hr.maria@carlsberg.local", "HR_MANAGER", "HR"),
            ("ro.auditor", "ro.auditor@carlsberg.local", "READ_ONLY", "IT"),
        ]

        for i in range(7):
            dept = random.choice(departments)
            uname = f"user{i+1}.{dept.lower()}"
            email = f"{uname}@carlsberg.local"
            role = "READ_ONLY" if dept != "IT" else random.choice(["IT_ADMIN", "READ_ONLY"])
            demo_users.append((uname, email, role, dept))

        created_count = 0

        for username, email, role, dept in demo_users:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"email": email, "is_staff": False}
            )
            if created:
                user.set_password("Carlsberg123!")
                user.save()
                created_count += 1

            user.groups.set([group_objs[role]])

            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.department = dept
            profile.job_title = random.choice(titles.get(dept, ["Employee"]))
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
