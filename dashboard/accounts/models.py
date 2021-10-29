from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Operator(AbstractUser):

    class RoleType(models.TextChoices):
        account_user = 'Accounts',_('Accounts')
        processing_user = 'Processing',_('Processing')
        packaging_user = 'Packaging',_('Packaging')
        delivery_user = 'Delivery',_('Delivery')
        admin = 'Admin',_('Admin')

    role = models.CharField(max_length=50,choices=RoleType.choices,default='Not Set')

    def __str__(self):
        return self.username


