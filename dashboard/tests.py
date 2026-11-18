from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser


class DashboardAccessTests(TestCase):
    def setUp(self):
        self.student = CustomUser.objects.create_user(
            username="stud", email="stud@example.com", password="Sturdy-Pass-2026", role=CustomUser.Role.STUDENT
        )
        self.instructor = CustomUser.objects.create_user(
            username="prof", email="prof@example.com", password="Sturdy-Pass-2026", role=CustomUser.Role.INSTRUCTOR
        )

    def test_logged_out_users_go_to_login(self):
        for name in ["dashboard", "student_dashboard", "instructor_dashboard"]:
            url = reverse(name)
            self.assertRedirects(self.client.get(url), f"{reverse('login')}?next={url}", msg_prefix=name)

    def test_dashboard_redirects_by_role(self):
        self.client.force_login(self.student)
        self.assertRedirects(self.client.get(reverse("dashboard")), reverse("student_dashboard"))
        self.client.force_login(self.instructor)
        self.assertRedirects(self.client.get(reverse("dashboard")), reverse("instructor_dashboard"))

    def test_student_cannot_open_instructor_dashboard(self):
        self.client.force_login(self.student)
        self.assertEqual(self.client.get(reverse("instructor_dashboard")).status_code, 403)

    def test_instructor_cannot_open_student_dashboard(self):
        self.client.force_login(self.instructor)
        self.assertEqual(self.client.get(reverse("student_dashboard")).status_code, 403)
