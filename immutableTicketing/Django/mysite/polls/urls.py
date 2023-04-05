from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.load_template, name='template'),
    path('send-transaction/', views.send_transaction, name='send transaction'),
]