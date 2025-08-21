from django.urls import path
from . import views

urlpatterns = [
    path("departments/", views.DepartmentCreateView.as_view()),
    path("employees/", views.EmployeeCreateView.as_view()),
    path("employees/<int:pk>/set-salary/", views.set_base_salary),
    path("leaves/update/", views.update_leave),
    path("salary/calculate/", views.calculate_salary),
    path("departments/<uuid:dept_id>/high-earners/", views.high_earners),
    path("high-earners/<str:month>/<str:year>/", views.high_earners_month),
]
