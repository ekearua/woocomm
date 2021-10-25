from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from .models import Operator

# Register your models here.
class OperatorUserAdmin(UserAdmin):
    list_display = ['username','role']

admin.site.register(Operator,OperatorUserAdmin)
