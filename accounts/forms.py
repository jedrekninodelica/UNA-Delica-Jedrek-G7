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


class ProfileForm(forms.ModelForm):
    """Lets users edit their own details. Role and username are not editable here."""

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "course", "contact_number", "profile_photo")
        widgets = {
            "contact_number": forms.TextInput(attrs={"placeholder": "09171234567"}),
            "profile_photo": forms.ClearableFileInput(attrs={"accept": "image/*"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("email", "first_name", "last_name"):
            self.fields[name].required = True

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        taken = CustomUser.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        if taken.exists():
            raise forms.ValidationError("Another account already uses this email.")
        return email

    def clean_profile_photo(self):
        photo = self.cleaned_data.get("profile_photo")
        if photo and hasattr(photo, "size") and photo.size > 2 * 1024 * 1024:
            raise forms.ValidationError("Photo must be 2 MB or smaller.")
        return photo
