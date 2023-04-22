from django.contrib import admin
from django.urls import path, include
from .views import homePage, eventPage, ownedTickets,singleTicket

urlpatterns = [
    path("", homePage.as_view(), name="home"),
    path("event/", eventPage.as_view(), name="events"),
    path("my-tickets/", ownedTickets.as_view(), name="myTickets"),
    path("ticket/<str:contract_address>/<int:ticket_index>", singleTicket.as_view(), name="single_ticket"),
    
]
