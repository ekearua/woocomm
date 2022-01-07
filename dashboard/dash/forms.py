from django import forms
from .models import Orders, Returns

acc_choices = [
        ('Pay On Delivery', 'pay_on_delivery'),
        ('Payment Confirmed', 'payment_confirmed'),
    ]

pack_choices = [
    ('Ready For Delivery','ready_for_delivery'),
    ('Ready For Pickup','ready_for_pickup'),
]

deliver_choices = [
    ('Order Delivered','order_delivered'),
    ('Order Picked Up', 'order_picked_up'),
]

shop_admin_choices = [
    ('Order Delivered','order_delivered'),
    ('Order Picked Up', 'order_picked_up')
]

order_choices = [
        ('Processing', 'processing'),
        ('On Hold', 'on_hold'),
        ('Pending', 'pending'),
        ('Payment Confirmed', 'payment_confirmed'),
        ('Pay On Delivery', 'pay_on_delivery'),
        ('Completed', 'completed'),
        ('Ready For Delivery','ready_for_delivery'),
        ('Ready For Pickup','ready_for_pickup'),
        ('Order Delivered', 'order_delivered'),
        ('Order Picked Up','order_picked_up'),
        ('Cancelled','cancelled'),
        ('Refunded','refunded')
    ]

class UpdateOrder(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(UpdateOrder, self).__init__(*args,**kwargs)

    class Meta:
        model = Orders
        fields = ['order_status','order_address']

        widgets = {
            'order_status': forms.Select(choices=order_choices)
        }

class AccOrder(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(AccOrder, self).__init__(*args,**kwargs)
        # self.fields['order_address'].widget.attrs['placeholder'] = self.fields['order_address'].label
    
    class Meta:
        model = Orders
        fields = ['order_status']        
        widgets = {
            'order_status': forms.Select(choices=acc_choices)
        }     
        
class PackOrder(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(PackOrder, self).__init__(*args,**kwargs)
        # self.fields['order_address'].widget.attrs['placeholder'] = self.fields['order_address'].label
    
    class Meta:
        model = Orders
        fields = ['order_status','order_address']        
        widgets = {
            'order_status': forms.Select(choices=pack_choices)
        }    

class DeliverOrder(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(DeliverOrder, self).__init__(*args,**kwargs)
        # self.fields['order_address'].widget.attrs['placeholder'] = self.fields['order_address'].label
    
    class Meta:
        model = Orders
        fields = ['order_status']
        widgets = {
            'order_status': forms.Select(choices=deliver_choices)
        } 

class ShopAdminOrder(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(ShopAdminOrder, self).__init__(*args,**kwargs)
        # self.fields['order_address'].widget.attrs['placeholder'] = self.fields['order_address'].label
    
    class Meta:
        model = Orders
        fields = ['order_status','order_address']        
        widgets = {
            'order_status': forms.Select(choices=order_choices)
        }       
class ReturnOrders(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(ReturnOrders, self).__init__(*args,**kwargs)

    class Meta:
        model = Returns
        fields=["return_id"]

class AccReturns(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(AccReturns, self).__init__(*args,**kwargs)
        # self.fields['order_address'].widget.attrs['placeholder'] = self.fields['order_address'].label
    
    class Meta:
        model = Returns
        fields = ['return_status']        
        widgets = {
            'return_status': forms.Select(choices=acc_choices)
        }     
        
class PackReturns(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(PackReturns, self).__init__(*args,**kwargs)
        # self.fields['order_address'].widget.attrs['placeholder'] = self.fields['order_address'].label
    
    class Meta:
        model = Returns
        fields = ['return_status']        
        widgets = {
            'order_status': forms.Select(choices=pack_choices)
        }    

class DeliverReturns(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(Returns, self).__init__(*args,**kwargs)
        # self.fields['order_address'].widget.attrs['placeholder'] = self.fields['order_address'].label
    
    class Meta:
        model = Returns
        fields = ['return_status']        
        widgets = {
            'return_status': forms.Select(choices=deliver_choices)
        } 

class ShopAdminReturns(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(ShopAdminReturns, self).__init__(*args,**kwargs)
        # self.fields['order_address'].widget.attrs['placeholder'] = self.fields['order_address'].label
    
    class Meta:
        model = Returns
        fields = ['return_status']        
        widgets = {
            'return_status': forms.Select(choices=shop_admin_choices)
        }
