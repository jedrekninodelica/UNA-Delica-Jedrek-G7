from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ["username", "email", "role", "is_staff"]