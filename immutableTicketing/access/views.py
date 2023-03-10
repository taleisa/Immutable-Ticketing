from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from . forms import accountForm
from . import models
from django.urls import reverse_lazy

class createAccount(FormView):
    template_name = "createAccount.html"
    success_url  = reverse_lazy('login')
    form_class = accountForm
    
    
    def form_valid(self, form):
        first_name = self.request.POST["first_name"]
        last_name = self.request.POST["last_name"]
        wallet_address = self.request.POST["wallet_address"]
        user,created = models.User.objects.get_or_create(wallet_address = wallet_address)
        if created:
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        return super(createAccount, self).form_valid(form)
        




class login(TemplateView):
    template_name = "login.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[""] = None
        return context
    


    