from django.contrib.admin import AdminSite
from django.shortcuts import redirect
from .rbac import is_it_or_superuser, is_readonly, is_rookie

class CarlsbergAdminSite(AdminSite):
    site_header = "Carlsberg Koprivnica – IT User Management"
    site_title = "Carlsberg Admin"
    index_title = "Administracija (samo IT)"

    def has_permission(self, request):
        user = request.user
        return is_it_or_superuser(user)

    def login(self, request, extra_context=None):
        """
        Ako netko pokuša na /admin, a nema prava:
        - READ_ONLY -> /
        - ROOKIE -> /training
        - ostali -> /
        """
        user = request.user
        if user.is_authenticated and not is_it_or_superuser(user):
            if is_rookie(user):
                return redirect("/training")
            return redirect("/")
        return super().login(request, extra_context)
