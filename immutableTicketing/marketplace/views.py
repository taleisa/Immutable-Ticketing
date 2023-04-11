from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy

class homePage(LoginRequiredMixin, TemplateView):
    template_name = 'marketplace/marketplacePage.html'
    login_url = reverse_lazy("login")

class eventPage(LoginRequiredMixin, TemplateView):
    template_name = 'marketplace/eventPage.html'
    login_url = reverse_lazy("events")