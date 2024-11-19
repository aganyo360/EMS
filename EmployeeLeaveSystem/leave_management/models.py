from django.contrib.auth.models import User
from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    short_name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or self.short_name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    emp_id = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    gender = models.CharField(max_length=100)
    dob = models.DateField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    address = models.TextField()
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=11)
    status = models.BooleanField(default=True)
    reg_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.emp_id})"


class LeaveType(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    to_date = models.DateField()
    from_date = models.DateField()
    description = models.TextField()
    posting_date = models.DateTimeField(auto_now_add=True)
    admin_remark = models.TextField(null=True, blank=True)
    admin_remark_date = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(choices=[
        (0, 'Pending'),
        (1, 'Approved'),
        (2, 'Rejected')
    ])
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.employee} - {self.leave_type.name}"


# Admin is tied to Django's User model, allowing it to manage users with Django's built-in permissions.
class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255)
    email = models.EmailField()
    updation_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fullname
