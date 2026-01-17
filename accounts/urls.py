from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("training", views.training, name="training"),
    path("it/", views.it_portal, name="it_portal"),
    path("hr/", views.hr_portal, name="hr_portal"),
    path("audit/", views.audit_portal, name="audit_portal"),
    path("sales/", views.sales_portal, name="sales_portal"),
    path("logout/", views.logout_view, name="logout"),

]
