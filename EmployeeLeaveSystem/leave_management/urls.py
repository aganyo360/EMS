from django.urls import path
from . import views

urlpatterns = [
    path("", views.employee_login, name="employee_login"),
    path('logout/', views.logout, name='logout'),

    path('dashboard', views.dashboard, name='dashboard'),
    path('employees', views.employees, name='employees'),
    path('add-employee', views.add_employee, name='add-employee'),
    path('update-employee', views.update_employee, name='update-employee'),
    path('department', views.department, name='department'),
    path('add-department', views.add_department, name='add-department'),
    path('leave-section', views.leave_section, name='leave-section'),
    path('add-leavetype', views.add_leavetype, name='add-leavetype'),
    path('pending-history', views.pending_history, name='pending-history'),
    path('approved-history', views.approved_history, name='approved-history'),
    path('declined-history', views.declined_history, name='declined-history'),
    path('leave-history', views.leave_history, name='leave-history'),
    path('manage-admin', views.manage_admin, name='manage-admin'),
    path('add-admin', views.add_admin, name='add-admin'),
    path('edit-department', views.update_department, name='update-department'),
    path('edit-leaveType', views.edit_leave_type, name='edit-leave-type'),
    path('employeeLeave-details', views.employeeLeave_details, name='employeeLeave-details'),

    
    path('leave/', views.leave, name='leave'),
    path('leave_history/', views.leave_history2, name='leave_history'),
    path('view_profile/', views.update_profile, name='view_profile'),
    path('change_password/', views.change_password, name='change_password'),

]
