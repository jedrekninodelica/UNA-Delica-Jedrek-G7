from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomerUserCreationForm

# Create your views here.

class SignUpView(CreateView):
    form_class = CustomerUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
