from django.urls import path

from .views import DashboardView, InstructorDashboardView, StudentDashboardView

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("student/", StudentDashboardView.as_view(), name="student_dashboard"),
    path("instructor/", InstructorDashboardView.as_view(), name="instructor_dashboard"),
]
