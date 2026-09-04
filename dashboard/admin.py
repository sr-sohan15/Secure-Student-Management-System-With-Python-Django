from django.contrib import admin
from .models import Student, StudentOTP

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'semester', 'cgpa', 'email', 'phone')
    search_fields = ('student_id', 'name', 'email')

@admin.register(StudentOTP)
class StudentOTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp_code', 'created_at')