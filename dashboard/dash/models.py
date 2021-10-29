from django.db import models
from django.conf import settings
from geopy import GoogleV3
from phonenumber_field.modelfields import PhoneNumberField
from pytz import timezone
from datetime import datetime
from django.urls import reverse
from .helper_db import order_list


# Create your models here.
geolocator = GoogleV3('AIzaSyAwqEbxprqVygh3fWlOl0blrQsxtj0bS4k')
class Orders(models.Model):

    order_choices = [
        ('processing', 'processing'),
        ('on-hold', 'on-hold'),
        ('payment confirmed', 'payment confirmed'),
        ('order paid', 'order-paid'),
        ('completed', 'completed'),
        ('cancelled','cancelled'),
        ('refunded', 'refunded'),
        ('failed', 'failed'),
        ('trash','trash')
    ]

    order_id = models.PositiveIntegerField(primary_key=True)
    order_first_name = models.CharField(max_length=50)
    order_last_name = models.CharField(max_length=50)
    order_email = models.EmailField()
    order_phone = PhoneNumberField()
    order_address = models.CharField(max_length=150)
    order_date_created = models.DateTimeField()
    order_payment_confirmation = models.BooleanField(default=True)
    order_date_paid = models.DateTimeField()
    order_amount = models.PositiveIntegerField()
    order_product = models.CharField(max_length=50)
    order_product_quantity = models.PositiveSmallIntegerField()
    order_product_price = models.PositiveSmallIntegerField()
    order_payment_method = models.CharField(max_length=50)
    order_delivery_type = models.CharField(max_length=50)
    order_delivery_date = models.CharField(max_length=255)
    order_status = models.CharField(max_length=50,choices=order_choices)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
    lat = models.DecimalField(max_digits=10,decimal_places=6,default=0)
    lon = models.DecimalField(max_digits=10,decimal_places=6,default=0)

    class Meta:
        ordering = ["-order_id"]
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def save(self,*args,**kwargs): 
        location = geolocator.geocode(self.order_address)
        if location is None:
            pass
        else:
            self.lat = location.latitude
            self.lon = location.longitude
        self.order_payment_confirmation = True       
        if str(self.order_date_paid).startswith('1899'):
            self.order_payment_confirmation = False                
        super(Orders, self).save(*args,**kwargs)
    
    def __str__(self):
        return self.order_id
    
    def get_absolute_url(self):
        return reverse("orders:all")

# [(Orders.save(order)) for order in Orders.objects.all()]

lagos = timezone('Africa/Lagos')
   
obj = [
    (Orders(
        order_id = order[0], 
        order_first_name = order[1],
        order_last_name = order[2],
        order_phone = order[3],
        order_email = order[4],
        order_address = order[5],
        order_date_created = lagos.localize(datetime.fromisoformat(order[6])),
        order_product = order[7],
        order_product_quantity = order[8],
        order_product_price = order[9],
        order_amount = order[10],
        order_date_paid = lagos.localize(datetime.fromisoformat(order[11])),
        order_payment_method = order[12],
        order_status = order[13],
        order_payment_confirmation= False,
        order_delivery_type = order[16],
        order_delivery_date = order[17]
        ))
        for order in order_list]

msg = Orders.objects.bulk_create(obj)

    
