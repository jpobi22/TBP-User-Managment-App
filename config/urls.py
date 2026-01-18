from django.urls import path, include
from accounts.views import it_dashboard
from accounts.admin import admin_site 
urlpatterns = [
    path("admin/", admin_site.urls),
    path("it-dashboard/", it_dashboard, name="it_dashboard"),
    path("", include("accounts.urls")),
]
