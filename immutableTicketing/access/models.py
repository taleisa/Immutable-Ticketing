from django.db import models
from django.contrib.auth.models import User


class web3User(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE,related_name='web3User')
    wallet_address = models.CharField(max_length = 42)
    is_admitted = models.BooleanField(default = False)

