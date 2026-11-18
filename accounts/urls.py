from django.urls import path

from .views import (
    ProfileUpdateView,
    ProfileView,
    SignUpView,
    UnaLoginView,
    UnaLogoutView,
    UnaPasswordChangeView,
)

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", UnaLoginView.as_view(), name="login"),
    path("logout/", UnaLogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
    path("password/change/", UnaPasswordChangeView.as_view(), name="password_change"),
]
