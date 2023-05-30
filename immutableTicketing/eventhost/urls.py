from django.urls import path
from . import views
from .views import dashboard, loginView, requests, signUp, tickets, eventRequestManegement, TicketRequest, signUpRequestManegement, LogoutView

urlpatterns = [
    path('dashboard/', dashboard.as_view(), name='dashboard'),
    path('login/', loginView.as_view(), name='eventhostlogin'),
    path('signup/', signUp.as_view(), name='eventhostsignup'),
    path('dashboard/requests', requests.as_view(), name='requests'),
    path('dashboard/ticketrequest', TicketRequest.as_view(), name='ticketrequest'),
    path('dashboard/eventrequestsmanagement', eventRequestManegement.as_view(), name='eventRequestManegement'),
    path('dashboard/signuprequestsmanagement', signUpRequestManegement.as_view(), name='signUpRequestManegement'),
    path('dashboard/<str:contract>/<int:id>', tickets.as_view(), name='tickets'),
    path('dashboard/logout', LogoutView.as_view(), name='eventhostlogout'),
]