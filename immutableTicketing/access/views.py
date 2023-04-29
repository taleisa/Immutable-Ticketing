from django.shortcuts import render
from django.views.generic import TemplateView, FormView, View
from django.contrib.auth.views import LoginView, LogoutView
from . forms import accountForm, loginForm, walletForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login, logout
from . models import web3User
from django.contrib import messages
from django.db import IntegrityError
from web3 import Web3
from django.http import HttpResponseRedirect
from immutableTicketing import settings

class createAccount(FormView):
    template_name = "access/createAccount.html"
    success_url  = reverse_lazy('login')
    form_class = accountForm
    def form_valid(self, form):
        form.save()
        return super(createAccount, self).form_valid(form)
        
class login(FormView):
    template_name = 'access/AppToNafath.html'
    success_url = reverse_lazy('home')
    form_class = walletForm
    def form_valid(self, form):
        wallet_address = form.cleaned_data['wallet_address'].lower()
        user = self.request.user
        if user.is_anonymous:# If non authenticated user
            messages.error(self.request, 'Please login using nafath')
            self.success_url = reverse_lazy('login')
            return super(login, self).form_valid(form)
        elif user.web3User.is_GEA or user.web3User.is_event_host:
            messages.error(self.request, 'Please use event host portal')
            self.success_url = reverse_lazy('login')
            return super(login, self).form_valid(form)
        try:# If user does not have aregistered wallet address will throw error
            user_wallet_address = user.web3User.wallet_address.lower()
        except:# User does not have wallet address
            webUser = web3User(user = user)
            webUser.wallet_address = Web3.to_checksum_address(wallet_address) 
            try:# Save user wallet
                webUser.save()
            except IntegrityError:# Other user has wallet address
                messages.error(self.request, 'Wallet registered to other user, please use your wallet')
            else:
                messages.success(self.request, 'Wallet has been saved')
            self.success_url = reverse_lazy('login')
        else:
            if user_wallet_address != wallet_address:
                messages.error(self.request, 'Please connect your registered wallet')
                self.success_url = reverse_lazy('login')
                return super(login, self).form_valid(form)
           
        return super(login, self).form_valid(form)

class nafath(LoginView):
    template_name = "access/nafathLoginV1.0.html"
    next_page = reverse_lazy('login')
    authentication_form = loginForm
    
    

class profilePage(LoginRequiredMixin,TemplateView):
    template_name = 'access/myProfile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context = {
            'name':user.get_full_name(),
            'email':user.email,
            'wallet':user.web3User.wallet_address
        }
        return context
    
class contactUs(LoginRequiredMixin,TemplateView):
    template_name = 'access/contactUs.html'
    
    
class logout(LogoutView):
    pass
