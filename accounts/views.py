from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomerUserCreationForm


class SignUpView(CreateView):
    form_class = CustomerUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


class UnaLoginView(auth_views.LoginView):
    # Uses templates/registration/login.html. A wrong username or password
    # shows Django's built-in error message on the form.
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Welcome back, {self.request.user.first_name or self.request.user.username}!")
        return response


class UnaLogoutView(auth_views.LogoutView):
    # Logout only works through POST (the button in the nav bar).
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.info(request, "You have been logged out.")
        return response
