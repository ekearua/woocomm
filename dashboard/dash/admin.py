from django.contrib import admin
from . import models 
# Register your models here.

class Order(admin.ModelAdmin):
    # fields = ['order_id','order_first_name','order_last_name','order_product','order_product_quantity','order_amount','order_payment_confirmation']
    list_display = ['order_id','order_first_name','order_last_name','order_product','order_product_quantity','order_amount','order_payment_confirmation','order_status']
    search_fields = ['order_id']
    # list_filter = ['state','inverter_code','inverter_capacity','type']  


admin.site.register(models.Orders,Order)