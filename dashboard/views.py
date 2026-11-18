from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView

from accounts.models import CustomUser


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Logged-out users are sent to the login page.
    Logged-in users with the wrong role get a 403 "Access denied" page.
    """

    required_role = None

    def test_func(self):
        return self.request.user.role == self.required_role


class DashboardView(LoginRequiredMixin, View):
    """After login, send each user to the dashboard for their role."""

    def get(self, request, *args, **kwargs):
        return redirect(request.user.dashboard_url_name)


class StudentDashboardView(RoleRequiredMixin, TemplateView):
    template_name = "dashboard/student.html"
    required_role = CustomUser.Role.STUDENT


class InstructorDashboardView(RoleRequiredMixin, TemplateView):
    template_name = "dashboard/instructor.html"
    required_role = CustomUser.Role.INSTRUCTOR

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["student_count"] = CustomUser.objects.filter(role=CustomUser.Role.STUDENT).count()
        return context
