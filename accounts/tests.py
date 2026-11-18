from django.test import TestCase
from django.urls import reverse

from .models import CustomUser

PASSWORD = "Sturdy-Pass-2026"


def make_user(username, role=CustomUser.Role.STUDENT, **extra):
    return CustomUser.objects.create_user(
        username=username,
        email=extra.pop("email", f"{username}@example.com"),
        password=PASSWORD,
        first_name="Test",
        last_name="User",
        role=role,
        **extra,
    )


class SignUpTests(TestCase):
    def post(self, **overrides):
        data = {
            "username": "juan",
            "email": "juan@example.com",
            "first_name": "Juan",
            "last_name": "Dela Cruz",
            "role": "STUDENT",
            "course": "BSIT-3",
            "password1": PASSWORD,
            "password2": PASSWORD,
        }
        data.update(overrides)
        return self.client.post(reverse("signup"), data, follow=True)

    def test_signup_success_hashes_password(self):
        response = self.post()
        user = CustomUser.objects.get(username="juan")
        self.assertNotEqual(user.password, PASSWORD)
        self.assertTrue(user.check_password(PASSWORD))
        self.assertEqual(user.role, CustomUser.Role.STUDENT)
        self.assertContains(response, "Account created")

    def test_required_fields(self):
        response = self.post(first_name="", email="")
        self.assertFalse(CustomUser.objects.exists())
        self.assertContains(response, "This field is required")

    def test_invalid_email_format(self):
        response = self.post(email="not-an-email")
        self.assertFalse(CustomUser.objects.exists())
        self.assertContains(response, "Enter a valid email address")

    def test_duplicate_username(self):
        make_user("juan", email="other@example.com")
        response = self.post()
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertContains(response, "already exists")

    def test_duplicate_email_case_insensitive(self):
        make_user("someone", email="juan@example.com")
        response = self.post(email="JUAN@example.com")
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertContains(response, "An account with this email already exists")

    def test_password_mismatch(self):
        response = self.post(password2="Different-Pass-2026")
        self.assertFalse(CustomUser.objects.exists())
        self.assertContains(response, "fields didn")  # "The two password fields didn't match."

    def test_invalid_role_rejected(self):
        self.post(role="ADMIN")
        self.assertFalse(CustomUser.objects.exists())


class LoginLogoutTests(TestCase):
    def setUp(self):
        self.student = make_user("stud")
        self.instructor = make_user("prof", role=CustomUser.Role.INSTRUCTOR)

    def test_invalid_credentials_show_error(self):
        response = self.client.post(reverse("login"), {"username": "stud", "password": "wrong"})
        self.assertContains(response, "Please enter a correct username and password")

    def test_student_lands_on_student_dashboard(self):
        response = self.client.post(reverse("login"), {"username": "stud", "password": PASSWORD}, follow=True)
        self.assertEqual(response.redirect_chain[-1][0], reverse("student_dashboard"))

    def test_instructor_lands_on_instructor_dashboard(self):
        response = self.client.post(reverse("login"), {"username": "prof", "password": PASSWORD}, follow=True)
        self.assertEqual(response.redirect_chain[-1][0], reverse("instructor_dashboard"))

    def test_logout_ends_session(self):
        self.client.force_login(self.student)
        self.client.post(reverse("logout"))
        url = reverse("student_dashboard")
        self.assertRedirects(self.client.get(url), f"{reverse('login')}?next={url}")


class ProfileTests(TestCase):
    def setUp(self):
        self.student = make_user("stud")
        self.other = make_user("other")

    def test_profile_requires_login(self):
        url = reverse("profile")
        self.assertRedirects(self.client.get(url), f"{reverse('login')}?next={url}")

    def test_view_own_profile_only(self):
        self.client.force_login(self.student)
        response = self.client.get(reverse("profile"))
        self.assertContains(response, "stud@example.com")
        self.assertNotContains(response, "other@example.com")

    def test_update_profile(self):
        self.client.force_login(self.student)
        response = self.client.post(
            reverse("profile_edit"),
            {
                "first_name": "Maria",
                "last_name": "Santos",
                "email": "maria@example.com",
                "course": "BSIT-3",
                "contact_number": "09171234567",
            },
            follow=True,
        )
        self.student.refresh_from_db()
        self.assertEqual(self.student.first_name, "Maria")
        self.assertEqual(self.student.contact_number, "09171234567")
        self.assertContains(response, "profile was updated")

    def test_cannot_take_another_users_email(self):
        self.client.force_login(self.student)
        response = self.client.post(
            reverse("profile_edit"),
            {"first_name": "A", "last_name": "B", "email": "other@example.com"},
        )
        self.assertContains(response, "Another account already uses this email")

    def test_role_cannot_be_changed_from_profile(self):
        self.client.force_login(self.student)
        self.client.post(
            reverse("profile_edit"),
            {"first_name": "A", "last_name": "B", "email": "stud@example.com", "role": "INSTRUCTOR"},
        )
        self.student.refresh_from_db()
        self.assertEqual(self.student.role, CustomUser.Role.STUDENT)
