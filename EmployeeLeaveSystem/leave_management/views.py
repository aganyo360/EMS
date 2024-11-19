from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import auth 
from .models import AdminProfile, Employee, Leave, LeaveType, Department
from django.utils.timezone import now

@login_required
def dashboard(request):
    if not request.user.is_superuser:
        return redirect('leave')
    context = {
        'leave_types_count': LeaveType.objects.count(),
        'employees_count': Employee.objects.filter(status=True).count(),
        'departments_count': Department.objects.count(),
        'pending_leaves_count': Leave.objects.filter(status=0).count(),
        'approved_leaves_count': Leave.objects.filter(status=1).count(),
        'declined_leaves_count': Leave.objects.filter(status=2).count(),
        'leaves':Leave.objects.filter()[:20]
    }
    return render(request, 'admin/dashboard.html', context)


@login_required
def employees(request):
    if not request.user.is_superuser:
        return redirect('leave')
    if 'inid' in request.GET:
        emp_id = request.GET['inid']
        employee = get_object_or_404(Employee, pk=emp_id)
        employee.status = False
        employee.save()
        messages.error(request, f"{employee.user.first_name} {employee.user.last_name} Has beed deactivated!")
        return redirect('employees')

    if 'id' in request.GET:
        emp_id = request.GET['id']
        employee = get_object_or_404(Employee, pk=emp_id)
        employee.status = True
        employee.save()
        messages.success(request, f"{employee.user.first_name} {employee.user.last_name} Has beed Activated!")

        return redirect('employees')
    
    employees_list = Employee.objects.all()

    return render(request, 'admin/employees.html', {'employees': employees_list})

@login_required
def add_employee(request):
    if not request.user.is_superuser:
        return redirect('leave')
    if request.method == "POST":
        emp_id = request.POST.get("empcode")
        first_name = request.POST.get("firstName")
        last_name = request.POST.get("lastName")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirmpassword")
        gender = request.POST.get("gender")
        dob = request.POST.get("dob")
        department_id = request.POST.get("department")
        address = request.POST.get("address")
        city = request.POST.get("city")
        country = request.POST.get("country")
        phone_number = request.POST.get("mobileno")

        if password != confirm_password:
            messages.error(request, "Password and Confirm Password do not match.")
            return redirect("add-employee")

        if Employee.objects.filter(emp_id=emp_id).exists():
            messages.error(request, "Employee ID already exists.")
            return redirect("add-employee")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("add-employee")

        user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)
        department = Department.objects.get(pk=department_id)

        employee = Employee.objects.create(
            user=user,
            emp_id=emp_id,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            dob=dob,
            department=department,
            address=address,
            city=city,
            country=country,
            phone_number=phone_number,
            status=True,
        )

        messages.success(request, "Employee added successfully!")
        return redirect("add-employee")

    departments = Department.objects.all()
    return render(request, "admin/add-employee.html", {"departments": departments})



@login_required
def department(request):
    if not request.user.is_superuser:
        return redirect('leave')
    if 'del' in request.GET:
        department_id = request.GET['del']
        department = get_object_or_404(Department, pk=department_id)
        department.delete()
        messages.success(request, "The selected department has been deleted.")
        return redirect('department')
    departments = Department.objects.all()
    context = {
        'departments': departments
    }
    return render(request, 'admin/department.html', context)


@login_required
def add_department(request):
    if not request.user.is_superuser:
        return redirect('leave')

    if request.method == 'POST':
        deptname = request.POST.get('departmentname')
        deptshortname = request.POST.get('departmentshortname')
        deptcode = request.POST.get('deptcode')

        if deptname and deptshortname and deptcode:
            try:
                Department.objects.create(
                    name=deptname,
                    short_name=deptshortname,
                    code=deptcode
                )
                messages.success(request, "Department Created Successfully")
            except Exception as e:
                messages.error(request, f"Something went wrong: {e}")
        else:
            messages.error(request, "All fields are required.")
    return render(request, 'admin/add-department.html')


@login_required
def leave_section(request):
    if not request.user.is_superuser:
        return redirect('leave')
    
    leave_id = request.GET.get('del')
    if leave_id:
        try:
            leave = LeaveType.objects.get(id=leave_id)
            leave.delete()
            messages.success(request, "Leave type record deleted.")
        except LeaveType.DoesNotExist:
            messages.error(request, "Leave type record not found.")

    leave_types = LeaveType.objects.all()

    return render(request, 'admin/leave-section.html', {'leave_types': leave_types})

@login_required
def add_leavetype(request):
    if not request.user.is_superuser:
        return redirect('leave')
    if request.method == 'POST':
        name = request.POST.get('leavetype')
        description = request.POST.get('description')

        if LeaveType.objects.filter(name=name).exists():
            messages.error(request, "Leave type already exists.")
        else:
            try:
                LeaveType.objects.create(name=name, description=description)
                messages.success(request, "Leave type added successfully.")
                return redirect('add-leavetype') 
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")

    return render(request, 'admin/add-leavetype.html')


@login_required
def pending_history(request):
    if not request.user.is_superuser:
        return redirect('leave')
    
    pending_leaves = Leave.objects.filter(status=0).select_related('employee').order_by('-id')
    return render(request, 'admin/pending-history.html', {'pending_leaves': pending_leaves})


@login_required
def approved_history(request):
    if not request.user.is_superuser:
        return redirect('leave')
    
    approved_leaves = Leave.objects.filter(status=1).order_by('-posting_date')
    
    return render(request, 'admin/approved-history.html', {'approved_leaves': approved_leaves})

@login_required
def declined_history(request):
    if not request.user.is_superuser:
        return redirect('leave')
    declined_leaves = Leave.objects.filter(status=2).order_by('-posting_date')
    
    return render(request, 'admin/declined-history.html', {'declined_leaves': declined_leaves})

@login_required
def leave_history(request):
    if not request.user.is_superuser:
        return redirect('leave')
    leave_records = Leave.objects.all().order_by('-id') 
    
    return render(request, 'admin/leave-history.html', {
        'leave_records': leave_records,
    })

@login_required
def manage_admin(request):
    if not request.user.is_superuser:
        return redirect('leave')
    
    if 'del' in request.GET:
        admin_id = request.GET['del']
        try:
            admin_to_delete = User.objects.get(id=admin_id)
            admin_to_delete.delete()
            messages.success(request, "The selected admin account has been deleted")
        except User.DoesNotExist:
            messages.error(request, "Admin account not found")
    admins = User.objects.filter(is_superuser=True).all()
    return render(request, 'admin/manage-admin.html', {'admins': admins})
  

@login_required
def add_admin(request):
    if not request.user.is_superuser:
        return redirect('leave')
    return render(request, 'admin/add-admin.html')


@login_required
def update_employee(request):
    if not request.user.is_superuser:
        return redirect('leave')
    employeeId =None
    if 'empid' in request.GET:
        employeeId = request.GET.get('empid')
    employee = get_object_or_404(Employee, id=employeeId)

    if request.method == 'POST':
        emp_id = request.POST.get("empcode")
        first_name = request.POST.get("firstName")
        last_name = request.POST.get("lastName")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirmpassword")
        gender = request.POST.get("gender")
        dob = request.POST.get("dob")
        department_id = request.POST.get("department")
        address = request.POST.get("address")
        city = request.POST.get("city")
        country = request.POST.get("country")
        phone_number = request.POST.get("mobileno")
        print(dob, "*"*80)
        employee.gender = gender
        employee.dob = dob
        employee.department = get_object_or_404(Department, id=department_id)
        employee.address = address
        employee.city = city
        employee.country = country
        employee.phone_number = phone_number
        employee.save()


        user = get_object_or_404(User, id=employee.user.id )
        user.first_name = first_name
        user.last_name = last_name
        if password == confirm_password and  password != '':
            user.set_password(password)
        else:
            messages.info(request, "Passwords not same")
        user.save()
        messages.success(request, "Updated successfully ")
        return redirect('update-employee')
    
    departments = Department.objects.all()
    
    return render(request, 'admin/update-employee.html', {"employee":employee, "departments":departments})




@login_required
def update_department(request):
    dept_id = request.GET.get('deptid')
    department = get_object_or_404(Department, id=dept_id)

    if request.method == "POST":
        dept_name = request.POST.get('departmentname')
        dept_short_name = request.POST.get('departmentshortname')
        dept_code = request.POST.get('deptcode')
        department.name = dept_name
        department.short_name = dept_short_name
        department.code = dept_code
        department.save()
        messages.success(request, "Department updated successfully!")
        return redirect(f'/edit-department?deptid={dept_id}')

    return render(request, 'admin/edit-department.html', {'department': department})

@login_required
def edit_leave_type(request):
    lid = request.GET.get('lid')
    leave_type = get_object_or_404(LeaveType, id=lid)

    if request.method == "POST":
        leavetype_name = request.POST.get("leavetype")
        description = request.POST.get("description")

        if not leavetype_name or not description:
            messages.error(request, "All fields are required.")
        else:
            leave_type.name = leavetype_name
            leave_type.description = description
            leave_type.save()
            messages.success(request, "Leave type updated successfully.")
            return redirect(f"/edit-leaveType?lid={lid}")

    return render(request, "admin/edit-leaveType.html", {"leave_type": leave_type})



@login_required
def employeeLeave_details(request):
    leave_id=request.GET.get('leaveid')
    leave = get_object_or_404(Leave, id=leave_id)
    
    if not leave.is_read:
        leave.is_read = True
        leave.save()

    if request.method == "POST":
        status = request.POST.get('status')
        description = request.POST.get('description')

        if status and description:
            leave.status = int(status)
            leave.admin_remark = description
            leave.admin_remark_date = now()
            leave.save()
            messages.success(request, "Leave updated successfully.")
        else:
            messages.error(request, "Please provide all required fields.")
        
        return redirect(f'/employeeLeave-details?leaveid={leave_id}')

    context = {
        "leave": leave
    }
    return render(request, "admin/employeeLeave-details.html", context)





def employee_login(request):
    next = request.GET.get('next') or None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)

            if user.is_superuser:
                # if not hasattr(user, 'admin_profile'):
                #     AdminProfile.objects.create(user=user)
                if next:
                    return redirect(next)
                return redirect('dashboard') 
            else:
                # if not hasattr(user, 'employee_profile'):
                #     Employee.objects.create(user=user)
                if next:
                        return redirect(next)
                return redirect('leave') 
        else:
            messages.error(request, "Invalid login credentials!")
    return render(request, 'login.html', {"message": None})


def logout(request):
    auth.logout(request)
    return redirect('employee_login')

@login_required
def leave(request):
    if request.method == 'POST':
        leavetype_id = request.POST.get('leavetype')
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        description = request.POST.get('description')
        if fromdate > todate:
            messages.error(request, "End date should be later than the start date!")
            return redirect('leave') 
        leave_type = LeaveType.objects.get(id=leavetype_id)
        Leave.objects.create(
            employee=request.user.employee,
            leave_type=leave_type,
            from_date=fromdate,
            to_date=todate,
            description=description,
            status=0, 
            is_read=False  
        )

        messages.success(request, "Your leave application has been submitted successfully.")
        return redirect('leave')

    return render(request, 'employees/leave.html', {
        'leave_types': LeaveType.objects.all(),
    })


@login_required
def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        user = request.user

        if not check_password(current_password, user.password):
            messages.error(request, "Your current password is incorrect.")
            return redirect("change_password")

        if new_password != confirm_password:
            messages.error(request, "New password and confirm password do not match.")
            return redirect("change_password")

        user.password = make_password(new_password)
        user.save()
        messages.success(request, "Your password has been updated successfully.")
        return redirect("leave")

    return render(request, "employees/change-password-employee.html")


@login_required
def leave_history2(request):
    employee = get_object_or_404(Employee, user=request.user )
    leaves = Leave.objects.filter(employee=employee).order_by('-posting_date')

    context = {
        'leaves': leaves,
    }
    return render(request, 'employees/leave-history.html', context)


@login_required
def update_profile(request):
    user = request.user
    employee = get_object_or_404(Employee, user=user)

    if request.method == "POST":
        first_name = request.POST.get("firstName")
        last_name = request.POST.get("lastName")
        gender = request.POST.get("gender")
        dob = request.POST.get("dob")
        department_id = request.POST.get("department")
        address = request.POST.get("address")
        city = request.POST.get("city")
        country = request.POST.get("country")
        phone_number = request.POST.get("mobileno")
        employee.first_name = first_name
        employee.last_name = last_name
        employee.gender = gender
        employee.dob = dob
        employee.department = get_object_or_404(Department, id=department_id)
        employee.address = address
        employee.city = city
        employee.country = country
        employee.phone_number = phone_number
        employee.save()

        messages.success(request, "Your record has been updated successfully.")
        return redirect("view_profile")

    departments = Department.objects.all()
    return render(request, "employees/my-profile.html", {"employee": employee, "departments": departments})

