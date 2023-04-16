from django.db import models
from django.contrib.auth.models import User


class web3User(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE,related_name='web3User')
    wallet_address = models.CharField(max_length = 42, unique=True)
    is_event_host = models.BooleanField(default = False)
    is_GEA = models.BooleanField(default = False)


class Event(models.Model):
    wallet_address = models.CharField(max_length = 42, unique=True)