from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from .forms import AccountsCreationForm


def home(request):
    return redirect('login/')


class AccountsCreateView(SuccessMessageMixin, CreateView):
    form_class = AccountsCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    success_message = "Your account was created successfully"

