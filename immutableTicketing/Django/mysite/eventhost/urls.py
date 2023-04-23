from django.urls import path
from . import views
from .views import dashboard, loginView, requests, signUp, tickets

urlpatterns = [
    path('dashboard/', dashboard.as_view(), name='dashboard'),
    path('login/', loginView.as_view(), name='login'),
    path('signup/', signUp.as_view(), name='signup'),
    path('dashboard/requests', requests.as_view(), name='requests'),
    path('dashboard/<str:contract>/<int:id>', tickets.as_view(), name='tickets'),
]