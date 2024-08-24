from django.contrib import admin
from django.contrib.auth.models import AbstractUser

from users.models import Users


from django.contrib.auth.hashers import make_password


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email',)
