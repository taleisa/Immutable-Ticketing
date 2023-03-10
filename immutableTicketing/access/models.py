from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    wallet_address = models.CharField(max_length=42, primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)