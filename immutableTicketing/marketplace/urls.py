from django.contrib import admin
from django.urls import path, include
from .views import homePage, eventPage, ownedTickets

urlpatterns = [
    path("", homePage.as_view(), name="home"),
    path("event/", eventPage.as_view(), name="events"),
    path("my-tickets/", ownedTickets.as_view(), name="myTickets"),
]
