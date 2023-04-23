from django import forms
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput, HiddenInput
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import web3User, SignUpRequest
from django.contrib.auth.models import User

class loginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget = forms.widgets.TextInput(
            attrs={
                "placeholder": "Username",
            }
        )
        self.fields["password"].widget = forms.widgets.PasswordInput(
            attrs={
                "placeholder": "Password",
            }
        )

#class signupForm(ModelForm):
#    class Meta:
#        model = SignUpRequest
#        fields = '__all__'
#        widgets = {
#            'companyName': TextInput(attrs={'placeholder':'Company Name'}),
#            'companyEmail': EmailInput(attrs={'placeholder':'Company Email'}),
#            'password1': PasswordInput(attrs={'placeholder':'Password'}),
#            'password2': PasswordInput(attrs={'placeholder':'Confirm Password'}),
#            'wallet_address': HiddenInput,
#        }        
class signupForm(forms.Form):
    companyName = forms.CharField(min_length=5, max_length=150, widget= forms.TextInput
                           (attrs={'placeholder':'Company Name'}))
    companyEmail = forms.EmailField(widget= forms.EmailInput
                           (attrs={'placeholder':'Company Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput
                                (attrs={'placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput
                                (attrs={'placeholder':'Confirm Password'}))
    walletAddress = forms.CharField(widget=forms.HiddenInput,min_length=42,max_length = 42, required=True, error_messages={
        'required': 'Please connect to Metamask' # errors for form: did not connect metamask
    })
        

            