from django import forms

class accountForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=20)
    last_name = forms.CharField(label='Last name', max_length=20)
    wallet_address = forms.CharField(widget=forms.HiddenInput(),max_length = 42)