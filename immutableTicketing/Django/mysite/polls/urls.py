from django.urls import path
from . import views
from .views import buyForm, success

urlpatterns = [
    path('home/', buyForm.as_view(), name='buy'),
    path('home/success/', success.as_view(), name='success'),
]