from django.contrib import admin

from accounts.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "first_name", "last_name", "is_active", "is_admin"]
    search_fields = ["email"]


admin.site.register(User, UserAdmin)
