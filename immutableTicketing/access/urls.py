from django.contrib import admin
from django.urls import path, include
from .views import createAccount, nafath, login, profilePage, contactUs, logout
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("signup/", createAccount.as_view(),name = 'signup'),
    path("login/nafath/",nafath.as_view() ,name = 'nafath'),
    path("login/",login.as_view(),name = 'login'),
    path("profile/",profilePage.as_view(),name = 'profile'),
    path("conatctUs/",contactUs.as_view(),name = 'contactUs'),
    path("logout/",logout.as_view(),name='logout'),
]

