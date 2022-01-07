from django.db import models
from django.conf import settings
from geopy import GoogleV3
from phonenumber_field.modelfields import PhoneNumberField
from pytz import timezone
from datetime import datetime
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
#from .helper_db import order_list


# Create your models here.
geolocator = GoogleV3('AIzaSyAwqEbxprqVygh3fWlOl0blrQsxtj0bS4k')
class Orders(models.Model):

    order_choices = [
        ('Processing', 'processing'),
        ('On hold', 'on_hold'),
        ('Pending', 'pending'),
        ('Payment confirmed', 'payment_confirmed'),
        ('Pay On Delivery', 'pay_on_delivery'),
        ('Completed', 'completed'),
        ('Ready For Delivery','ready_for_delivery'),
        ('Ready For Pickup','ready_for_pickup'),
        ('Order Delivered', 'order_delivered'),
        ('Order Picked Up','order_picked_up'),
        ('Refunded','refunded'),
        ('Cancelled','cancelled')
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
    # order_delivery_date = models.CharField(max_length=255)
    order_status = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
    lat = models.DecimalField(max_digits=10,decimal_places=6,default=0)
    lon = models.DecimalField(max_digits=10,decimal_places=6,default=0)
    coupon_no = models.CharField(max_length=50,default='-')

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
        else:
            self.order_payment_confirmation = True
        if self.coupon_no != '-':
            try:
                returns = Returns.objects.get(voucher_number = self.coupon_no)
                refund = RefundOrders(refund_id=self.order_id,return_details=returns,order_details=self)
                refund.save()
            except ObjectDoesNotExist:
                pass
        super(Orders, self).save(*args,**kwargs)
    
    def __str__(self):
        return str(self.order_id)
    
    def get_absolute_url(self):
        return reverse("orders:all")

# [(Orders.save(order)) for order in Orders.objects.all()]

# lagos = timezone('Africa/Lagos')
   
#obj = [
 #   (Orders(
 #       order_id = order[0], 
 #       order_first_name = order[1],
 #       order_last_name = order[2],
 #       order_phone = order[3],
 #       order_email = order[4],
 #       order_address = order[5],
 #       order_date_created = lagos.localize(datetime.fromisoformat(order[6])),
 #       order_product = order[7],
 #       order_product_quantity = order[8],
 #       order_product_price = order[9],
 #       order_amount = order[10],
 #       order_date_paid = lagos.localize(datetime.fromisoformat(order[11])),
 #       order_payment_method = order[12],
 #       order_status = order[13],
 #       order_payment_confirmation= False,
 #       order_delivery_type = order[16],
 #       order_delivery_date = order[17]
 #       ))
 #       for order in order_list]

#msg = Orders.objects.bulk_create(obj)

class Returns(models.Model):
    return_id = models.PositiveIntegerField(primary_key=True)
    ticket_number = models.CharField(max_length=50)
    voucher_number = models.CharField(max_length=50)
    return_status = models.CharField(max_length=50)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE,null=True,blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)

    class Meta:
        ordering = ["-ticket_number"]
        verbose_name = 'return'
        verbose_name_plural = 'returns'

    def save(self,*args,**kwargs):
        super(Returns, self).save(*args,**kwargs)

    def __str__(self):
        return str(self.order_ticket_number)

    def get_absolute_url(self):
        return reverse("orders:returns")

class RefundOrders(models.Model):
    refund_id = models.PositiveIntegerField(primary_key=True)
    return_details = models.ForeignKey(Returns,on_delete=models.CASCADE)
    order_details = models.ForeignKey(Orders,on_delete=models.CASCADE,null=True,blank=True)
    class Meta:
        ordering = ["refund_id"]
        verbose_name = 'refund'
        verbose_name_plural = 'refunds'

    def save(self,*args,**kwargs): 
        super(RefundOrders, self).save(*args,**kwargs)
    
    def __str__(self):
        return str(self.refund_id)
    
    def get_absolute_url(self):
        return reverse("orders:refunds")
