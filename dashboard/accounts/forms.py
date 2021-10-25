from . import models
from django.contrib.auth.forms import UserCreationForm

class OperatorSignupForm(UserCreationForm):

    class Meta:
        fields= ('first_name','last_name','username','email','role','password1','password2')
        model = models.Operator

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label = 'Display Name'
        self.fields['email'].label = 'E-mail Address'
    