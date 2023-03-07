from django.contrib.auth.models import Group
from rest_framework import permissions

# https://stackoverflow.com/questions/19372553/django-rest-framework-check-user-is-in-group


def is_in_group(user, group_name):
    try:
        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
    except Group.DoesNotExist:
        return None


class HasGroupPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        required_groups_mapping = getattr(view, "required_groups", {})
        required_groups = required_groups_mapping.get(request.method, [])
        return any([is_in_group(request.user, group_name) for group_name in required_groups])
