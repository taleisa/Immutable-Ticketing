from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from . forms import accountForm, loginForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy

class createAccount(FormView):
    template_name = "createAccount.html"
    success_url  = reverse_lazy('login')
    form_class = accountForm
    def form_valid(self, form):
        form.save()
        # username = self.request.POST["username"]
        # password = self.request.POST["password"]
        # wallet_address = self.request.POST["wallet_address"]
        # user,created = User.objects.create()
        # if created:
        #     user.username = username
        #     user.password = password
        #     user.web3User.wallet_address = wallet_address
        #     user.save()
        return super(createAccount, self).form_valid(form)
        




class login(FormView):
    form_class = loginForm
    template_name = "login.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[""] = None
        return context
    


    