from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'email')
    fieldsets = (
        ('User info', {'fields': ('username',
         'email', 'first_name', 'last_name', 'bio')}),
        ('Permissions', {'fields': ('is_staff', 'role')}),
        ('Email verification', {'fields': ('confirmation_code',)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
