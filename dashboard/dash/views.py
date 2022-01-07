from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
#from django.views.generic.base import RedirectView
from .models import Orders,Returns
from django.urls import reverse
from django.utils.decorators import method_decorator
from woocommerce import API
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from pytz import timezone as timez
from datetime import datetime,timedelta
from django.contrib.auth import get_user_model
from django.utils import timezone as tz
from django.contrib.auth.mixins import LoginRequiredMixin
from carts.models import Carts
from .forms import AccOrder,PackOrder,DeliverOrder,ShopAdminOrder,UpdateOrder,ReturnOrders, DeliverReturns, ShopAdminReturns, PackReturns, AccReturns
# Create your views here.

wcapi = API(
            url="http://waraqata.com/", # Your store URL
            consumer_key="ck_40067fcf6aecc329b6e5fb3ee4ac8ff86a4edabd", # Your consumer key
            consumer_secret="cs_4128f8b5b5cc3a1dc62719b2d5cfc2f88f57bb7e", # Your consumer secret
            wp_api=True, # Enable the WP REST API integration
            version="wc/v3", # WooCommerce WP REST API version
            timeout=30)


class OrderList(LoginRequiredMixin,ListView):
    model = Orders
    fields = ['order_id','order_first_name','order_last_name','order_product','order_product_quantity','order_amount','order_payment_confirmation']
    template_name = 'orders_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["acc_list"] = ['processing','pending','on-hold','Cancelled','Refunded','Awaiting Coupon']
        context["del_list"] = ['Ready For Delivery','Ready For Pickup','Refunded','Cancelled']
        context["pack_list"] = ['Payment Confirmed','Pay On Delivery','Refunded','Cancelled']
        return context

    def get_queryset(self):
        return Orders.objects.order_by('-order_id')
    
class OrderDetail(LoginRequiredMixin,DetailView):
    model = Orders
    # template_name = 'orders_detail.html'

class OrderUpdate(LoginRequiredMixin,UpdateView):
    model = Orders
    form = UpdateOrder
    #User = get_user_model()
    fields = ['order_address','order_status']
    
    def form_valid(self,form):
        if form.is_valid():
            self.object.user = self.request.user
        #pk = str(self.object.pk)
        #wcapi = API(
                #url="http://waraqata.com/", # Your store URL
                #consumer_key="ck_40067fcf6aecc329b6e5fb3ee4ac8ff86a4edabd", # Your consumer key
                #consumer_secret="cs_4128f8b5b5cc3a1dc62719b2d5cfc2f88f57bb7e", # Your consumer secret
                #wp_api=True, # Enable the WP REST API integration
                #version="wc/v3", # WooCommerce WP REST API version
                #timeout=30)

        #data = {
            #"status": status_data
            #}
        #wcapi.post("orders/"+pk, data)
        self.object.save()
        return super().form_valid(form)

class UpdateDB(ListView):
    template_name = 'orders_list_db.html'
    model = Orders
    fields = ['order_id','order_first_name','order_last_name','order_product','order_product_quantity','order_amount','order_payment_confirmation']
    
    def get_queryset(self):  
        return Orders.objects.order_by('-order_id')

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(UpdateDB, self).dispatch(*args, **kwargs)
    
    @method_decorator(csrf_exempt)
    def post(self,request,*args,**kwargs):
        all_orders = wcapi.get('orders',params={"per_page": 100}).json()
        orderss = Orders.objects.all()
        print(len(orderss))
        if (len(orderss) != len(all_orders)):
            new_num =  len(all_orders)-len(orderss)
            all_orders = all_orders[:new_num]        
            print(new_num)
            order_list = [[order['id'],order['billing']['first_name'],order['billing']['last_name'],order['billing']['phone'],
                order['billing']['email'],order['shipping']['address_1'],order['date_created'],
                order['line_items'][0]['name'],order['line_items'][0]['quantity'],order['line_items'][0]['price'],
                int(float(order['total'])),order['date_paid'],order['payment_method_title'],order['status'],
                order['shipping_lines'][0]['method_title'],order['coupon_lines'][0]['code']] for order in all_orders]
            order_list = [['1900-01-01T00:00:00' if ode is None else ode for ode in order]for order in order_list]
            lagos = timez('Africa/Lagos')
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
            order_delivery_type = order[14],
            coupon_no = order[15]
	    ))
            for order in order_list]
        
            if new_num > 1:
                Orders.objects.bulk_create(obj)
                [Orders.save(order) for order in orderss[:new_num]]
                emails = [order[4] for order in order_list]
                try:
                    for i in range(len(emails)):
                        cars = Carts.objects.filter(time_added__gte=tz.now()-timedelta(minutes=30),customer_email=emails[i],cart_status='in_progress')
                        cars_1 = Carts.objects.filter(time_added__gte=tz.now()-timedelta(minutes=30),cart_status='in_progress')
                        cars_rec = Carts.objects.filter(time_added__gte=tz.now()-timedelta(minutes=30),customer_email=emails[i],cart_status='abandoned')
                        cars.update(cart_status='completed')
                        cars_1.update(cart_status='abandoned')
                        cars_rec.update(cart_status = 'recovered')
                except ObjectDoesNotExist:
                    pass
            else:
                try:
                    email = order_list[4]
                    cars = Carts.objects.filter(time_added__gte=tz.now()-timedelta(minutes=30),customer_email=order_list[4],cart_status='in_progress')
                    cars_1 = Carts.objects.filter(time_added__gte=tz.now()-timedelta(minutes=30),cart_status='in_progress')
                    cars_rec = Carts.objects.filter(time_added__gte=tz.now()-timedelta(minutes=30),customer_email=email,cart_status='in_progress')
                    cars.update(cart_status='completed')
                    cars_1.update(cart_status='abandoned')
                    cars_rec.update(cart_status = 'recovered')
                except ObjectDoesNotExist:
                    pass
            Orders.save(obj[0])
            obj[0].refresh_from_db()
            # [Orders.save(order, update_fields=['lat','lon']) for order in orderss[:new_num]]
            return redirect('/orders/')
        return redirect('/orders/')

def get_del_order(request,pk):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        order = get_object_or_404(Orders,pk=pk)
        form = DeliverOrder(request.POST, instance=order)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            data = form.cleaned_data
            form.instance.user = request.user
            form.instance.order_status = data['order_status']
            form.save()
            returns = Returns.objects.get(pk=pk)
            returns.return_status = 'Completed'
            # redirect to a new URL:
            return HttpResponseRedirect('/orders/')

    # if a GET (or any other method) we'll create a blank form
    else:
        order = Orders.objects.get(pk=pk)
        form = DeliverOrder(instance=order)
        order_key = pk
        # print(order_key)

    return render(request, 'dash/delivery_update.html', {'form': form,'pk':order_key})

def get_acc_order(request,pk):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        order = get_object_or_404(Orders,pk=pk)
        form = AccOrder(request.POST, instance=order)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            data = form.cleaned_data
            form.instance.user = request.user
            form.instance.order_status = data['order_status']
            # form.instance.order_address = data['order_address']
            
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/orders/')

    # if a GET (or any other method) we'll create a blank form
    else:
        order = Orders.objects.get(pk=pk)
        form = AccOrder(instance=order)
        order_key = pk
        # print(order_key)

    return render(request, 'dash/accounts_update.html', {'form': form,'pk':order_key})

def get_pack_order(request,pk):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        order = get_object_or_404(Orders,pk=pk)
        form = PackOrder(request.POST, instance=order)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            data = form.cleaned_data
            form.instance.user = request.user
            form.instance.order_status = data['order_status']
            form.instance.order_address = data['order_address']
            
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/orders/')

    # if a GET (or any other method) we'll create a blank form
    else:
        order = Orders.objects.get(pk=pk)
        form = PackOrder(instance=order)
        order_key = pk
        # print(order_key)

    return render(request, 'dash/package_update.html', {'form': form,'pk':order_key})

def get_shopadmin_order(request,pk):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        order = get_object_or_404(Orders,pk=pk)
        form = ShopAdminOrder(request.POST, instance=order)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            data = form.cleaned_data
            form.instance.user = request.user
            form.instance.order_status = data['order_status']
            form.instance.order_address = data['order_address']
            
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/orders/')

    # if a GET (or any other method) we'll create a blank form
    else:
        order = Orders.objects.get(pk=pk)
        form = ShopAdminOrder(instance=order)
        order_key = pk
        # print(order_key)

    return render(request, 'dash/shopadmin_update.html', {'form': form,'pk':order_key})

def update_order(request,pk):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        order = get_object_or_404(Orders,pk=pk)
        form = UpdateOrder(request.POST, instance=order)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            data = form.cleaned_data
            form.instance.user = request.user
            form.instance.order_status = data['order_status']
            form.instance.order_address = data['order_address']

            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/orders/')

    # if a GET (or any other method) we'll create a blank form
    else:
        order = Orders.objects.get(pk=pk)
        form = UpdateOrder(instance=order)
        order_key = pk
        # print(order_key)
    return render(request, 'dash/orders_form.html', {'form': form,'pk':order_key})
def process_request(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:        
        form = ReturnOrders(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            data = form.cleaned_data
            order = get_object_or_404(Orders,order_id=form.data['return_id'])
            form.instance.user = request.user
            form.instance.return_status = "Awaiting Coupon"
            form.instance.order = order
            form.instance.processing_date = tz.now()
            store = order.order_date_created
            store_1 = form.instance.processing_date
            form.instance.ticket_number = str(data['return_id']) + '/'+ str(store.year)[-2:] + str(store.month) + str(store.day) + '/' +str(store_1.year)[-2:] + str(store_1.month) + str(store_1.day)

            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/orders/returns/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ReturnOrders()
        
    return render(request, 'dash/process_returns.html', {'form': form})

class ReturnDetail(LoginRequiredMixin,DetailView):
    model = Returns
    # template_name = 'dash/return_detail.html'

class ReturnList(LoginRequiredMixin,ListView):
    model = Returns
    fields = ['return_ticket','order']
    template_name = 'dash/returns.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["acc_list"] = ['processing','pending','on-hold','Cancelled','Refunded','Awaiting Coupon']
        context["del_list"] = ['Ready For Delivery','Ready For Pickup','Refunded','Cancelled']
        context["pack_list"] = ['Payment Confirmed','Pay On Delivery','Refunded','Cancelled']
        context["adv_list"] = ['Awaiting Coupon','Coupon Generated']
        return context

    # def get_queryset(self):
    #     return Returns.objects.order_by('-order_id')

def get_del_return(request,pk):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        order = get_object_or_404(Returns,pk=pk)
        form = DeliverReturns(request.POST, instance=order)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            data = form.cleaned_data
            form.instance.user = request.user
            form.instance.return_status = data['return_status']
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/orders/returns/')

    # if a GET (or any other method) we'll create a blank form
    else:
        order = Returns.objects.get(pk=pk)
        form = DeliverReturns(instance=order)
        order_key = pk

    return render(request, 'dash/delivery_update.html', {'form': form,'pk':order_key})

def get_acc_return(request,pk):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        order = get_object_or_404(Returns,pk=pk)
        form = AccReturns(request.POST, instance=order)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            data = form.cleaned_data
            form.instance.user = request.user
            form.instance.return_status = data['return_status']
            # form.instance.order_address = data['order_address']

            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/orders/returns/')

    # if a GET (or any other method) we'll create a blank form
    else:
        order = Returns.objects.get(pk=pk)
        form = AccReturns(instance=order)
        order_key = pk

    return render(request, 'dash/accounts_update.html', {'form': form,'pk':order_key})

def get_pack_return(request,pk):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        order = get_object_or_404(Returns,pk=pk)
        form = PackReturns(request.POST, instance=order)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            data = form.cleaned_data
            form.instance.user = request.user
            form.instance.return_status = data['order_status']

            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/orders/returns/')

    # if a GET (or any other method) we'll create a blank form
    else:
        order = Returns.objects.get(pk=pk)
        form = PackReturns(instance=order)
        order_key = pk
        # print(order_key)

    return render(request, 'dash/package_update.html', {'form': form,'pk':order_key})

def get_shopadmin_return(request,pk):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        order = get_object_or_404(Orders,pk=pk)
        form = ShopAdminReturns(request.POST, instance=order)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            data = form.cleaned_data
            form.instance.user = request.user
            form.instance.order_status = data['order_status']

            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/orders/')

    # if a GET (or any other method) we'll create a blank form
    else:
        order = Returns.objects.get(pk=pk)
        form = ShopAdminReturns(instance=order)
        order_key = pk
        # print(order_key)

    return render(request, 'dash/shopadmin_update.html', {'form': form,'pk':order_key}) 

def create_coupon(request,pk):
    returns = Returns.objects.get(pk=pk)
    returns.voucher_number = str(pk) + "REF"
    returns.return_status = "Coupon Generated"
    returns.save(update_fields=["voucher_number","return_status"])
    amount = returns.order.order_product_price
    data = {
        "code": str(pk) + "REF",
        "amount": amount,
        "exclude_sale_items": False,
        "usage_limit": 1,
        "description": "Order" + str(pk) + "Refund Coupon"
    }

    wcapi.post("coupons", data).json()
    return HttpResponseRedirect(reverse('orders:returns'))
