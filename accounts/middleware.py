from django.db import connection, transaction

class PgChangedByMiddleware:
   
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(request, "user", None) and request.user.is_authenticated:
            changed_by = request.user.username
        else:
            changed_by = "anonymous"

        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute("SELECT set_config('app.changed_by', %s, true);", [changed_by])

            response = self.get_response(request)

        return response
