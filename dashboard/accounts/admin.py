from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from .models import Operator

# Register your models here.
class OperatorUserAdmin(UserAdmin):
    list_display = ['username','role']
    fieldsets = (
        (None, {
            'fields': ('username', 'password','role')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        #('Additional info', {
         #   'fields': ('role')
        #})
    )

admin.site.register(Operator,OperatorUserAdmin)
