from django.db import models
from django.contrib.auth.models import User


class web3User(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE,related_name='web3User')
    wallet_address = models.CharField(max_length = 42, unique=True)
    is_event_host = models.BooleanField(default = False)
    is_GEA = models.BooleanField(default = False)

class Event(models.Model):
    event_host = models.ForeignKey(web3User, on_delete=models.CASCADE)
    address = models.CharField(max_length=42, unique=True)

class SignUpRequest(models.Model):
    companyName = models.CharField(max_length=150, unique=True)
    companyEmail = models.EmailField(max_length=50, unique=True)
    password1 = models.CharField(max_length=50)
    password2 = models.CharField(max_length=50)
    wallet_address = models.CharField(max_length = 42, unique=True)

class EventRequest(models.Model):
    event_host = models.ForeignKey(web3User, on_delete=models.CASCADE)
    eventName = models.CharField(max_length=30, unique=True)
    eventSymbol = models.CharField(max_length=8)
    eventLocation = models.CharField(max_length=30)
    eventStartDate = models.DateTimeField()
    eventEndDate = models.DateTimeField()
    eventType = models.CharField(max_length=30)
    
class Gate(models.Model):
    address = models.CharField(max_length = 42, unique=True)