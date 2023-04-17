from django import forms

class buyForm(forms.Form):
    event_name = forms.CharField(label="Event Name",max_length=200)
    wallet_address = forms.CharField(widget=forms.HiddenInput,max_length = 42)