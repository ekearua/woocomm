from django.contrib import admin
from . import models 
# Register your models here.

class Order(admin.ModelAdmin):
    # fields = ['order_id','order_first_name','order_last_name','order_product','order_product_quantity','order_amount','order_payment_confirmation']
    list_display = ['order_id','order_first_name','order_last_name','order_product','order_product_quantity',
                   'order_amount','order_address','order_date_created','order_delivery_type',
                   'lat','lon','user','order_status']
    search_fields = ['order_id']
    # list_filter = ['state','inverter_code','inverter_capacity','type']

class Return(admin.ModelAdmin):
    list_display = ['return_id','ticket_number','voucher_number','order','user','return_status']
    search_fields = ['return_id']


admin.site.register(models.Orders,Order)
admin.site.register(models.Returns,Return)
