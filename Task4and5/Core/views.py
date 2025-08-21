from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import F
from .models import Department, Employee, LeaveApplication
from .serializers import DepartmentSerializer, EmployeeSerializer, LeaveSerializer

# 1. POST API to create a department
@api_view(["POST"])
def create_department(request):
    serializer = DepartmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

# 2. POST API to create an employee
@api_view(["POST"])
def create_employee(request):
    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

# 3. POST API to set base salary
@api_view(["POST"])
def set_salary(request, emp_id):
    try:
        emp = Employee.objects.get(id=emp_id)
        emp.baseSalary = request.data.get("baseSalary")
        emp.save()
        return Response({"message": "Salary updated"})
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=404)

# 4. UPDATE API to increase leave
@api_view(["PUT"])
def update_leave(request, emp_id):
    month = request.data.get("month")
    year = request.data.get("year")
    leaves = int(request.data.get("leaves", 0))

    leave_app, created = LeaveApplication.objects.get_or_create(
        employee_id=emp_id, month=month, year=year
    )
    leave_app.leaves = F("leaves") + leaves
    leave_app.save()
    leave_app.refresh_from_db()
    return Response({"message": "Leave updated", "leaves": leave_app.leaves})

# 5. POST API calculate payable salary
@api_view(["POST"])
def calculate_salary(request, emp_id):
    month = request.data.get("month")
    year = request.data.get("year")

    try:
        emp = Employee.objects.get(id=emp_id)
        leave = LeaveApplication.objects.filter(employee=emp, month=month, year=year).first()
        leave_count = leave.leaves if leave else 0
        deduction = leave_count * (emp.baseSalary / 25)
        payable = emp.baseSalary - deduction
        return Response({"employee": emp.name, "payable_salary": payable})
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=404)

# 6. GET API high earners in department
@api_view(["GET"])
def high_earners(request, dept_id):
    employees = Employee.objects.filter(department_id=dept_id).order_by("-baseSalary")
    top_salaries = sorted(set(employees.values_list("baseSalary", flat=True)), reverse=True)[:3]
    high = employees.filter(baseSalary__in=top_salaries)
    serializer = EmployeeSerializer(high, many=True)
    return Response(serializer.data)

# 7. GET API high earners in specific month
@api_view(["GET"])
def high_earners_month(request, month, year):
    salaries = []
    for emp in Employee.objects.all():
        leave = LeaveApplication.objects.filter(employee=emp, month=month, year=year).first()
        leave_count = leave.leaves if leave else 0
        deduction = leave_count * (emp.baseSalary / 25)
        payable = emp.baseSalary - deduction
        salaries.append((emp, payable))

    top_pay = sorted(set([s for _, s in salaries]), reverse=True)[:3]
    high = [emp for emp, sal in salaries if sal in top_pay]
    serializer = EmployeeSerializer(high, many=True)
    return Response(serializer.data)
