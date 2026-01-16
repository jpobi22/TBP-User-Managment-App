from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Count
from .models import AuditLog

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
