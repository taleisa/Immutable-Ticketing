from django.contrib import admin
from django.urls import path, include
from .views import createAccount, nafath, login
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("signup/", createAccount.as_view(),name = 'signup'),
    path("login/nafath/",nafath.as_view() ,name = 'nafath'),
    path("login/",login.as_view(),name = 'login'),
]

