from django.shortcuts import HttpResponseRedirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from .models import Orders 
from django.urls import reverse
from django.utils.decorators import method_decorator
from woocommerce import API
from django.views.decorators.csrf import csrf_exempt
from pytz import timezone
from datetime import datetime
from django.contrib.auth import  get_user_model

# Create your views here.
class OrderList(generic.ListView):
    model = Orders
    fields = ['order_id','order_first_name','order_last_name','order_product','order_product_quantity','order_amount','order_payment_confirmation']
    template_name = 'orders_list.html'

    def get_queryset(self):        
        return Orders.objects.order_by('-order_id')

class OrderDetail(generic.DetailView):
    model = Orders
    # template_name = 'orders_detail.html'

class OrderUpdate(UpdateView):
    model = Orders
    User = get_user_model()
    fields = ['order_status']
    
    def form_valid(self,form):        
        if form.is_valid():
            status_data = form.cleaned_data['order_status']
            status_data = str(status_data).lower()
            self.object.user = self.request.user
        pk = str(self.object.pk)
        wcapi = API(
                url="http://waraqata.com/", # Your store URL
                consumer_key="ck_40067fcf6aecc329b6e5fb3ee4ac8ff86a4edabd", # Your consumer key
                consumer_secret="cs_4128f8b5b5cc3a1dc62719b2d5cfc2f88f57bb7e", # Your consumer secret
                wp_api=True, # Enable the WP REST API integration
                version="wc/v3", # WooCommerce WP REST API version
                timeout=30)

        data = {
            "status": status_data
            }
        wcapi.post("orders/"+pk, data)
        self.object.save()
        return super().form_valid(form)

# @method_decorator(csrf_exempt, name='post')
class UpdateDB(CreateView):
    template_name = 'orders_dbupdate.html'
    model = Orders
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(UpdateDB, self).dispatch(*args, **kwargs)

    @method_decorator(csrf_exempt)
    def post(self,request,*args,**kwargs):
        wcapi = API(
            url="http://waraqata.com/", # Your store URL
            consumer_key="ck_40067fcf6aecc329b6e5fb3ee4ac8ff86a4edabd", # Your consumer key
            consumer_secret="cs_4128f8b5b5cc3a1dc62719b2d5cfc2f88f57bb7e", # Your consumer secret
            wp_api=True, # Enable the WP REST API integration
            version="wc/v3", # WooCommerce WP REST API version
            timeout=30)
        all_orders = wcapi.get('orders',params={"per_page": 100}).json()
        orderss = Orders.objects.all()
        print(len(all_orders),len(orderss))
        if (len(orderss) != len(all_orders)):
            new_num =  len(all_orders)-len(orderss)        
            print(new_num)
            order_list = [[order['id'],order['billing']['first_name'],order['billing']['last_name'],order['billing']['phone'],
                    order['billing']['email'],order['billing']['address_1'],order['date_created'],
                    order['line_items'][0]['name'],order['line_items'][0]['quantity'],order['line_items'][0]['price'],
                    int(float(order['total'])),order['date_paid'],order['payment_method_title'],order['status'],
                    order['shipping_lines']] for order in all_orders]
            order_list = [['1900-01-01T00:00:00' if ode is None else ode for ode in order]for order in order_list]
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
            order_delivery_type = order[14][0]['method_title']))
            for order in order_list]
        
            if new_num > 1:
                Orders.objects.bulk_create(obj)
            else:
                Orders.save(obj[0])
            print('done')
            [Orders.save(order, update_fields=['order_payment_confirmation']) for order in orderss[:new_num]]
        # [Orders.save(order, update_fields=['order_payment_confirmation']) for order in orderss]
        return HttpResponseRedirect(reverse('orders:all'))



        
        

    
        
        
        



    
    
