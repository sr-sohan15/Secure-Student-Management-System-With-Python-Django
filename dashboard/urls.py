from django.contrib import admin
from django.urls import path
from dashboard.views import (
    dashboard_view, 
    export_students_csv, 
    edit_student_view, 
    student_custom_login_view, 
    admin_custom_login_view,
    student_verify_otp_view, 
    student_portal_view, 
    student_signup_view, 
    student_logout_view, 
    delete_student_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', student_custom_login_view, name='student_login'),
    path('accounts/login/', student_custom_login_view, name='login'), # 👈 জ্যাঙ্গোর ডিফল্ট রিডাইরেক্ট ফিক্স করার জন্য এই রাউটটি জরুরি
    path('student/login/', student_custom_login_view, name='student_login_url'),
    path('admin-login/', admin_custom_login_view, name='admin_login'),
    path('verify-otp/', student_verify_otp_view, name='student_verify_otp'),
    path('student/', student_portal_view, name='student_portal'),
    path('student/portal/', student_portal_view, name='student_portal_url'),
    path('signup/', student_signup_view, name='student_signup'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('export-csv/', export_students_csv, name='export_csv'),
    path('edit/<int:pk>/', edit_student_view, name='edit_student'),
    path('delete/<int:pk>/', delete_student_view, name='delete_student'),
    path('logout/', student_logout_view, name='student_logout'),
]