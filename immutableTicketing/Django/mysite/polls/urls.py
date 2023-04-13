from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.load_template, name='template'),
    path('home/<account>', views.send_transaction, name='send transaction'),
]