from django import forms
from .models import Orders

class UpdateOrder(forms.ModelForm):
    
    class Meta:
        model = Orders
        fields = ['order_status']

        widgets = {
            'order_status': forms.CheckboxSelectMultiple()
        }