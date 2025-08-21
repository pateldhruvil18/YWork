from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import F
from .models import Department, Employee, LeaveApplication
from .serializers import DepartmentSerializer, EmployeeSerializer, LeaveApplicationSerializer

# 1. POST Create Department
class DepartmentCreateView(generics.CreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

# 2. POST Create Employee
class EmployeeCreateView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

# 3. POST Set Base Salary
@api_view(["POST"])
def set_base_salary(request, pk):
    try:
        emp = Employee.objects.get(pk=pk)
        emp.baseSalary = request.data.get("baseSalary")
        emp.save()
        return Response({"message": "Base salary updated"})
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=404)

# 4. UPDATE API to increase leave count
@api_view(["PUT"])
def update_leave(request):
    emp_id = request.data.get("employeeId")
    month = request.data.get("month")
    year = request.data.get("year")
    leaves = int(request.data.get("leaves", 0))

    leave, created = LeaveApplication.objects.get_or_create(employee_id=emp_id, month=month, year=year)
    leave.leaves += leaves
    leave.save()
    return Response({"message": "Leave updated", "leaves": leave.leaves})

# 5. POST Payable salary
@api_view(["POST"])
def calculate_salary(request):
    emp_id = request.data.get("employeeId")
    month = request.data.get("month")
    year = request.data.get("year")

    try:
        emp = Employee.objects.get(id=emp_id)
        leave = LeaveApplication.objects.filter(employee=emp, month=month, year=year).first()
        total_leaves = leave.leaves if leave else 0
        payable = emp.baseSalary - (total_leaves * (emp.baseSalary // 25))
        return Response({"payableSalary": payable})
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=404)

# 6. GET High earners in department
@api_view(["GET"])
def high_earners(request, dept_id):
    employees = Employee.objects.filter(department_id=dept_id).order_by("-baseSalary")
    unique_salaries = sorted(list(set(employees.values_list("baseSalary", flat=True))), reverse=True)[:3]
    top_emps = employees.filter(baseSalary__in=unique_salaries)
    return Response(EmployeeSerializer(top_emps, many=True).data)

# 7. GET High earners in a specific month
@api_view(["GET"])
def high_earners_month(request, month, year):
    # Similar logic, but check salary after leave deductions
    data = []
    for emp in Employee.objects.all():
        leave = LeaveApplication.objects.filter(employee=emp, month=month, year=year).first()
        total_leaves = leave.leaves if leave else 0
        payable = emp.baseSalary - (total_leaves * (emp.baseSalary // 25))
        data.append({"id": emp.id, "name": emp.name, "payableSalary": payable, "department": str(emp.department.id)})

    top_salaries = sorted(list(set([d["payableSalary"] for d in data])), reverse=True)[:3]
    result = [d for d in data if d["payableSalary"] in top_salaries]
    return Response(result)
