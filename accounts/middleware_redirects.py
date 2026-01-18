from django.shortcuts import redirect
from django.urls import resolve
from .rbac import is_readonly, is_rookie

class AccessRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        
        if response.status_code == 403 and request.user.is_authenticated:
            if is_rookie(request.user):
                return redirect("/training")
            if is_readonly(request.user) or True:
                return redirect("/")
        return response
