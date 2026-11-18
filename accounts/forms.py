from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomerUserCreationForm(UserCreationForm):
    """Sign-up form. UserCreationForm checks that both passwords match and hashes the password."""

    role = forms.ChoiceField(
        label="I am a",
        choices=CustomUser.Role.choices,
        widget=forms.RadioSelect,
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email", "first_name", "last_name", "role", "course")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("email", "first_name", "last_name"):
            self.fields[name].required = True
        self.fields["course"].help_text = "Optional, e.g. BSIT-3"

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

