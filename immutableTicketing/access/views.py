from django.shortcuts import render
from django.views.generic import TemplateView, FormView, View
from django.contrib.auth.views import LoginView
from . forms import accountForm, loginForm, walletForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from . models import web3User

class createAccount(FormView):
    template_name = "createAccount.html"
    success_url  = reverse_lazy('login')
    form_class = accountForm
    def form_valid(self, form):
        form.save()
        return super(createAccount, self).form_valid(form)
        
class login(FormView):
    template_name = 'AppToNafathV2.0.html'
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        wallet_address = form.cleaned_data['wallet_address']
        user = self.request.user
        try:
            user.web3user.wallet_address
            
        except:
            web3User = web3User()
            web3User.wallet_address = wallet_address
            web3User.user = user
            web3User.save()
        return super(createAccount, self).form_valid(form)

class nafath(LoginView):
    template_name = "nafathLoginV1.0.html"
    next_page = reverse_lazy('login')
    authentication_form = loginForm
    # def form_valid(self, form):
    #     username = form.cleaned_data['J_username']
    #     password = form.cleaned_data['J_password']
    #     user = authenticate(self.request,username = username, password = password)
    #     if user is not None:
    #         login(self.request,user)
    #         return super(login, self).form_valid(form)

class homePage(LoginRequiredMixin, TemplateView):
    template_name = 'homePage.html'
    login_url = reverse_lazy("login")
