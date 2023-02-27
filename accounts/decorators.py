from functools import wraps

from django.shortcuts import redirect


def unauthenticated_user_required(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("about")
        else:
            return function(request, *args, **kwargs)
    return wrapper
