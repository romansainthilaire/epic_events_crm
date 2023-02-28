from functools import wraps

from django.core.exceptions import PermissionDenied


def allowed_groups(groups=[]):
    def decorator(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.first().name
            if group in groups:
                return function(request, *args, **kwargs)
            else:
                raise PermissionDenied()
        return wrapper
    return decorator
