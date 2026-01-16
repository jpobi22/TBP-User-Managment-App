from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, permission_required

from django.shortcuts import render
from django.db.models import Count
from .models import AuditLog
from .models import AuditLog, UserProfile


@staff_member_required
def it_dashboard(request):
    recent = AuditLog.objects.all()[:50]

    by_table = (
        AuditLog.objects.values("table_name")
        .annotate(cnt=Count("id"))
        .order_by("-cnt")[:10]
    )

    by_action = (
        AuditLog.objects.values("action")
        .annotate(cnt=Count("id"))
        .order_by("-cnt")
    )

    context = {
        "recent": recent,
        "by_table": by_table,
        "by_action": by_action,
    }
    return render(request, "accounts/it_dashboard.html", context)

@login_required
@permission_required("accounts.access_it_portal", raise_exception=True)
def it_portal(request):
    return render(request, "accounts/it_portal.html")

@login_required
@permission_required("accounts.access_hr_portal", raise_exception=True)
def hr_portal(request):
    profiles = UserProfile.objects.select_related("user").order_by("department", "user__username")[:50]
    return render(request, "accounts/hr_portal.html", {"profiles": profiles})

@login_required
@permission_required("accounts.access_sales_portal", raise_exception=True)
def sales_portal(request):
    return render(request, "accounts/sales_portal.html")

@login_required
@permission_required("accounts.access_audit_portal", raise_exception=True)
def audit_portal(request):
    recent = AuditLog.objects.all()[:100]
    return render(request, "accounts/audit_portal.html", {"recent": recent})