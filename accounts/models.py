from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

phone_validator = RegexValidator(
    regex=r"^(\+63|0)9\d{9}$",
    message="Enter a PH mobile number like 09171234567 or +639171234567.",
)


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        INSTRUCTOR = "INSTRUCTOR", "Instructor"

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.STUDENT,
    )

    # Email is required and unique (username is still used to log in).
    email = models.EmailField("email address", unique=True)

    course = models.CharField("course / program", max_length=100, blank=True)
    contact_number = models.CharField(max_length=13, blank=True, validators=[phone_validator])
    profile_photo = models.ImageField(upload_to="profile_photos/", blank=True)

    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    @property
    def is_instructor(self):
        return self.role == self.Role.INSTRUCTOR

    @property
    def dashboard_url_name(self):
        return "instructor_dashboard" if self.is_instructor else "student_dashboard"
