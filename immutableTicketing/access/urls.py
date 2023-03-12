from django.contrib import admin
from django.urls import path, include
from .views import createAccount, login

urlpatterns = [
    path("signup/", createAccount.as_view(),name = 'signup'),
    path("login/", login.as_view(),name = 'login'),
    # path("home_page/", home_page.as_view(),name = 'home_page'),
]

