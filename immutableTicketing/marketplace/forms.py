from django import forms
from access.models import web3User
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm



class listForm(forms.Form):
    ticket_index = forms.IntegerField( widget = forms.HiddenInput)
    contract_address = forms.CharField(widget=forms.HiddenInput, max_length=42)
