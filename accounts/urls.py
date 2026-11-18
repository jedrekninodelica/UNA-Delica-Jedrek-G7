from django.urls import path

from .views import (
    SignUpView,
    UnaLoginView,
    UnaLogoutView,
)

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", UnaLoginView.as_view(), name="login"),
    path("logout/", UnaLogoutView.as_view(), name="logout"),
]
