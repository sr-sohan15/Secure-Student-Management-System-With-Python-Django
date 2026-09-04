from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
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
    
    # স্টুডেন্ট পোর্টাল ও লগইন রাউটস
    path('', student_custom_login_view, name='student_login'),
    path('student/login/', student_custom_login_view, name='student_login_url'),
    path('student/', student_portal_view, name='student_portal'),
    path('student/portal/', student_portal_view, name='student_portal_url'),
    
    # এডমিন ড্যাশবোর্ড ও লগইন রাউটস
    path('dashboard/', dashboard_view, name='dashboard'),
    path('admin-login/', admin_custom_login_view, name='admin_login'),
    
    # পাসওয়ার্ড রিসেট রাউটস
    path('admin/password_reset/', auth_views.PasswordResetView.as_view(template_name='dashboard/password_reset.html'), name='admin_password_reset'),
    path('admin/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='dashboard/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='dashboard/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='dashboard/password_reset_complete.html'), name='password_reset_complete'),
    
    # অন্যান্য কমন রাউটস
    path('verify-otp/', student_verify_otp_view, name='student_verify_otp'),
    path('signup/', student_signup_view, name='student_signup'),
    path('export-csv/', export_students_csv, name='export_csv'),
    path('edit/<int:pk>/', edit_student_view, name='edit_student'),
    path('delete/<int:pk>/', delete_student_view, name='delete_student'),
    path('logout/', student_logout_view, name='student_logout'),
]

# 👈 মিডিয়া ফাইল সার্ভ করার জন্য এই লাইনটি অত্যন্ত জরুরি
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)