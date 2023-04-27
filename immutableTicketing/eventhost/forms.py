from django import forms
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput, HiddenInput, formset_factory
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
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
class TicketForm(forms.Form):
    name = forms.CharField(max_length=30, widget= forms.TextInput
                           (attrs={'placeholder':'Ticket Class'}))
    uri = forms.CharField(max_length=500, widget= forms.TextInput
                           (attrs={'placeholder':'Ticket Uri'}))
    seatNumberStart = forms.IntegerField(widget= forms.NumberInput
                           (attrs={'placeholder':'Ticket Seat Number (From)'}))
    price = forms.DecimalField(decimal_places=6, widget= forms.NumberInput
                           (attrs={'placeholder':'Ticket Price in ETH'}))
    quantity = forms.IntegerField(widget= forms.NumberInput
                           (attrs={'placeholder':'Number of Tickets'}))
    contractAddress = forms.CharField(widget=forms.HiddenInput,min_length=42,max_length = 42, required=True, error_messages={
        'required': 'Please choose event' # errors for form: did not choose event
    })
    
class eventrequestForm(forms.Form):
    eventName = forms.CharField(min_length=5, max_length=30, widget= forms.TextInput
                           (attrs={'placeholder':'Event Name'}))
    eventSymbol = forms.CharField(min_length=3, max_length=5, widget= forms.TextInput
                           (attrs={'placeholder':'Event Symbol'}))
    eventLocation = forms.CharField(min_length=5, max_length=30, widget= forms.TextInput
                           (attrs={'placeholder':'Event Location'}))
    eventType = forms.CharField(min_length=5, max_length=30, widget= forms.TextInput
                           (attrs={'placeholder':'Event Type'}))
    eventStartDate = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder': 'Event Start Date and Time'}))
    eventEndDate = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder': 'Event End Date and Time'}))
    #tickets = formset_factory(TicketForm, extra=1)

class requestManagementForm(forms.Form):
    status = forms.CharField(widget=forms.HiddenInput, required=True) 
    requestId = forms.IntegerField(widget=forms.HiddenInput, required=True)    
    
        
        

            