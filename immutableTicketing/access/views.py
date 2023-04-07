from django.shortcuts import render
from django.views.generic import TemplateView, FormView, View
from django.contrib.auth.views import LoginView
from . forms import accountForm, loginForm, walletForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login
from . models import web3User
from django.contrib import messages

class createAccount(FormView):
    template_name = "createAccount.html"
    success_url  = reverse_lazy('login')
    form_class = accountForm
    def form_valid(self, form):
        form.save()
        return super(createAccount, self).form_valid(form)
        
class login(FormView):
    template_name = 'AppToNafath.html'
    success_url = reverse_lazy('home')
    form_class = walletForm
    def form_valid(self, form):
        wallet_address = form.cleaned_data['wallet_address']
        user = self.request.user
        if user.is_anonymous:
            messages.error(self.request, 'Please login using nafath')
            self.success_url = reverse_lazy('login')
            return super(login, self).form_valid(form)
        try:
            user_wallet_address = user.web3User.wallet_address
        except:
            webUser = web3User(user = user)
            webUser.wallet_address = wallet_address
            webUser.save()
            messages.success(self.request, 'Wallet has been saved')
            self.success_url = reverse_lazy('login')
        else:
            if user_wallet_address != wallet_address:
                messages.error(self.request, 'Please connect your regidtered wallet')
                self.success_url = reverse_lazy('login')
                return super(login, self).form_valid(form)
           
        return super(login, self).form_valid(form)

class nafath(LoginView):
    template_name = "nafathLoginV1.0.html"
    next_page = reverse_lazy('login')
    authentication_form = loginForm
    
    

