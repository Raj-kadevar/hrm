from django.contrib import admin
from django.contrib.auth import get_user_model

from user.models import Device

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (["username", "email", "profile"])


@admin.register(Device)
class Device(admin.ModelAdmin):
    list_display = ["name"]