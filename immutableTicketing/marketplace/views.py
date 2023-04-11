from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.views import View
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

class homePage(LoginRequiredMixin, TemplateView):
    template_name = 'marketplace/marketplacePage.html'
    login_url = reverse_lazy("login")

class eventPage(LoginRequiredMixin, TemplateView):
    template_name = 'marketplace/eventPage.html'
    login_url = reverse_lazy("events")
    
class ownedTickets(LoginRequiredMixin,TemplateView):
    template_name  = 'marketplace/myTicket.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        ticket1 = {'Title':'Kevin hart Stand up comedy','Time':'4:00PM','Location':'Boulevard','Date':'17/3/2026'}
        ticket2 = {'Title':'Kevin hart Stand up comedy','Time':'4:00PM','Location':'Boulevard','Date':'17/3/2026'}
        all_tickets = [ticket1,ticket2]
        context["tickets"] = all_tickets
        return context
    
    
    
class listTicket(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        ticket_address = args['address']
        ###################################################
        ####Invoke transaction to list ticket on blockchain
        ###################################################
        return HttpResponseRedirect('myTickets')