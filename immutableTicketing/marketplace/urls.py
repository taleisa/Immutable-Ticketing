from django.contrib import admin
from django.urls import path, include
from .views import homePage

urlpatterns = [
    path("home/",homePage.as_view(),name = 'home')
]

