from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Operator(AbstractUser):

    class RoleType(models.TextChoices):
        account_user = 'Accounts',_('Accounts')
        shop_manager = 'Shop Manager',_('Shop Manager')
        packaging_user = 'Packaging',_('Packaging')
        delivery_user = 'Delivery',_('Delivery')
        admin = 'Admin',_('Admin')
        not_set = 'Not Set',_('Unverified User'),
        customer_advocacy = 'Customer Advocacy',_('Customer Advocacy')

    role = models.CharField(max_length=50,choices=RoleType.choices,default='Not Set')

    def __str__(self):
        return self.username


