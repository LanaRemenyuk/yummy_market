from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "name", "surname", "email")
    search_fields = ("email", "username")
    list_filter = ("email", "username")
    empty_value_display = "-no_info_to_display-"