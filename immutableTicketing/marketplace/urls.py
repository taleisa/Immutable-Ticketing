from django.contrib import admin
from django.urls import path, include
from .views import homePage, eventPage, ownedTickets,singleTicket,eventTickets, marketplace

urlpatterns = [
    path("", homePage.as_view(), name="home"),
    path("marketplace/", marketplace.as_view(), name="marketplace"),
    path("marketplace/<str:contract_address>", marketplace.as_view(), name="marketplace"),
    path("event/<str:contract_address>", eventPage.as_view(), name="event"),
    path("my-tickets/", ownedTickets.as_view(), name="myTickets"),
    path("ticket/<str:contract_address>/<int:ticket_index>", singleTicket.as_view(), name="single_ticket"),
    path("event/<str:contract_address>/tickets", eventTickets.as_view(), name="event_tickets"),
]
