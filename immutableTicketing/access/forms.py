from django import forms
from django.contrib.auth.forms import UserCreationForm  
from access.models import web3User
from django.contrib.auth.models import User
class accountForm(UserCreationForm):
    username = forms.CharField(label='username', min_length=5, max_length=150)  
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)  
    wallet_address = forms.CharField(widget=forms.HiddenInput,max_length = 42, required=True)
    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username  
    def wallet_address_clean(self):
        wallet_address = self.cleaned_data['wallet_address']
        web3User = web3User.objects.get(wallet_address = wallet_address)
        if web3User:
            raise ValidationError("Address already in use")
        return wallet_address  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  
  
    def save(self, commit = True):
        user = User.objects.create_user(  
            username = self.cleaned_data['username'],   
            password = self.cleaned_data['password1'],  
        )
        web3User.objects.create(user = user, wallet_address = self.cleaned_data['wallet_address'])  
        return user  

class loginForm(forms.Form):
    wallet_address = forms.CharField(widget=forms.HiddenInput(),max_length = 42,required=True)

    # def __init__(self, request,*args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super(loginForm, self).__init__(*args, **kwargs)


    # def get_user():
    #     print("herefromgetuser")
    #     user = web3AuthBackend.authenticate(wallet_address = wallet_address)
    #     return user

