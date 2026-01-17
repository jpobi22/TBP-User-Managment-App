from django.contrib.auth.models import AnonymousUser

def is_it_or_superuser(user) -> bool:
    if not user or isinstance(user, AnonymousUser) or not user.is_authenticated:
        return False
    return user.is_superuser or user.groups.filter(name="IT").exists() or user.groups.filter(name="IT_ADMIN").exists()

def is_readonly(user) -> bool:
    return bool(user and user.is_authenticated and user.groups.filter(name__in=["READ_ONLY", "readonly"]).exists())

def is_rookie(user) -> bool:
    return bool(user and user.is_authenticated and user.groups.filter(name__in=["ROOKIE", "rookie"]).exists())
