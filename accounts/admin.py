from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import AuditLog
from .models import UserProfile

admin.site.site_header = "Carlsberg Koprivnica – IT User Management"
admin.site.site_title = "Carlsberg Koprivnica Admin"
admin.site.index_title = "Upravljanje korisnicima, ulogama i pravima (IT Odjel)"

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    extra = 0

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "department", "job_title", "is_active_employee", "updated_at")
    search_fields = ("user__username", "user__email", "department", "job_title")
    list_filter = ("department", "is_active_employee")

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("occurred_at", "table_name", "action", "row_pk", "changed_by")
    list_filter = ("table_name", "action")
    search_fields = ("row_pk", "changed_by", "table_name")
    date_hierarchy = "occurred_at"
    ordering = ("-occurred_at",)

    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False