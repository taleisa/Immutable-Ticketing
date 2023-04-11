from django.contrib import admin
from django.urls import path, include
from .views import homePage, eventPage, ownedTickets,listTicket

urlpatterns = [
    path("",homePage.as_view(),name = 'home'),
    path("event/",eventPage.as_view(),name = 'events'),
    path("myTickets/",ownedTickets.as_view(),name = 'myTickets'),
    path("listTicket/<str:address>/",listTicket.as_view(),name = 'sellTicket'),
]