from functools import wraps

from django.http import Http404


def unauthenticated_user_required(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            raise Http404
        else:
            return function(request, *args, **kwargs)
    return wrapper
