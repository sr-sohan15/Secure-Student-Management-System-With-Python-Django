import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Avg
import random
from .models import Student, StudentOTP
from .forms import (
    StudentLoginForm, 
    AdminLoginForm, 
    StudentOTPVerifyForm, 
    StudentSignUpForm, 
    AdminAddStudentForm
)

@login_required(login_url='admin_login')
def dashboard_view(request):
    if not request.user.is_superuser:
        return redirect('student_portal')

    if request.method == 'POST':
        form = AdminAddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = AdminAddStudentForm()
        
    query = request.GET.get('q', '')
    if query:
        students = Student.objects.filter(name__icontains=query) | Student.objects.filter(student_id__icontains=query)
    else:
        students = Student.objects.all()
        
    total_students = Student.objects.count()
    avg_cgpa = Student.objects.aggregate(Avg('cgpa'))['cgpa__avg']
    avg_cgpa = round(avg_cgpa, 2) if avg_cgpa else 0.00
    
    avg_sgpa = Student.objects.aggregate(Avg('sgpa'))['sgpa__avg']
    avg_sgpa = round(avg_sgpa, 2) if avg_sgpa else 0.00

    context = {
        'students': students,
        'form': form,
        'total_students': total_students,
        'avg_cgpa': avg_cgpa,
        'avg_sgpa': avg_sgpa,
        'query': query,
    }
    return render(request, 'dashboard/index.html', context)


@login_required(login_url='admin_login')
def export_students_csv(request):
    if not request.user.is_superuser:
        return redirect('student_portal')
        
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student_records.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Student ID', 'Name', 'Semester', 'CGPA', 'SGPA', 'Email', 'Phone'])
    
    students = Student.objects.all()
    for student in students:
        writer.writerow([student.student_id, student.name, student.semester, student.cgpa, student.sgpa, student.email, student.phone])
        
    return response


@login_required(login_url='admin_login')
def edit_student_view(request, pk):
    if not request.user.is_superuser:
        return redirect('student_portal')
        
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = AdminAddStudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = AdminAddStudentForm(instance=student)
        
    return render(request, 'dashboard/edit_student.html', {'form': form, 'student': student})


def student_custom_login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('dashboard')
        return redirect('student_portal')

    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['student_id'].strip()
            
            if student_id.lower() == 'admin':
                return redirect('admin_login')
            
            try:
                student = Student.objects.get(student_id=student_id)
            except Student.DoesNotExist:
                form.add_error('student_id', 'Student ID not found. Please contact admin.')
                return render(request, 'dashboard/student_login.html', {'form': form})
            
            user, created = User.objects.get_or_create(
                username=student_id, 
                defaults={'email': student.email}
            )
            
            if user.email != student.email:
                user.email = student.email
                user.save()

            otp_code = str(random.randint(100000, 999999))
            StudentOTP.objects.filter(user=user).delete()
            StudentOTP.objects.create(user=user, otp_code=otp_code)

            print("\n" + "="*40)
            print(f"🔑 STUDENT LOGIN OTP FOR ID [{student_id}]: {otp_code}")
            print("="*40 + "\n")

            try:
                send_mail(
                    subject='Your Student Portal Login OTP',
                    message=f'Hello {student.name},\n\nYour OTP is: {otp_code}',
                    from_email=None,
                    recipient_list=[student.email],
                    fail_silently=True,
                )
            except Exception as e:
                pass

            request.session['student_login_user_id'] = user.id
            return redirect('student_verify_otp')
    else:
        form = StudentLoginForm()
    
    return render(request, 'dashboard/student_login.html', {'form': form})


def admin_custom_login_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].strip()
            password = form.cleaned_data['password']
            
            admin_user = authenticate(request, username=username, password=password)
            
            if admin_user is None or not admin_user.is_superuser:
                form.add_error('password', 'Invalid admin username or password.')
                return render(request, 'dashboard/admin_login.html', {'form': form})

            otp_code = str(random.randint(100000, 999999))
            StudentOTP.objects.filter(user=admin_user).delete()
            StudentOTP.objects.create(user=admin_user, otp_code=otp_code)

            print("\n" + "="*40)
            print(f"🔑 ADMIN LOGIN OTP FOR [{username}]: {otp_code}")
            print("="*40 + "\n")

            try:
                send_mail(
                    subject='Your Admin Portal Secure Login OTP',
                    message=f'Hello Admin {username},\n\nYour Login OTP is: {otp_code}',
                    from_email=None,
                    recipient_list=[admin_user.email],
                    fail_silently=True,
                )
            except Exception as e:
                pass

            request.session['student_login_user_id'] = admin_user.id
            return redirect('student_verify_otp')
    else:
        form = AdminLoginForm()
    
    return render(request, 'dashboard/admin_login.html', {'form': form})


def student_verify_otp_view(request):
    user_id = request.session.get('student_login_user_id')
    if not user_id:
        return redirect('student_login')
    
    user = User.objects.get(id=user_id)
    
    if request.method == 'POST':
        form = StudentOTPVerifyForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp_code']
            try:
                otp_record = StudentOTP.objects.get(user=user, otp_code=entered_otp)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                otp_record.delete()
                if 'student_login_user_id' in request.session:
                    del request.session['student_login_user_id']
                
                if user.is_superuser:
                    return redirect('dashboard')
                return redirect('student_portal')
            except StudentOTP.DoesNotExist:
                form.add_error('otp_code', 'Invalid OTP code. Please try again.')
    else:
        form = StudentOTPVerifyForm()
        
    return render(request, 'dashboard/student_verify_otp.html', {'form': form, 'student_id': user.username})


@login_required(login_url='student_login')
def student_portal_view(request):
    if request.user.is_superuser:
        try:
            current_student = Student.objects.first()
        except Student.DoesNotExist:
            current_student = None
    else:
        try:
            current_student = Student.objects.get(student_id=request.user.username)
        except Student.DoesNotExist:
            current_student = None
        
    return render(request, 'dashboard/student_portal.html', {'current_student': current_student})


def student_signup_view(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            
            Student.objects.create(
                name=user.get_full_name() or user.username,
                student_id=form.cleaned_data.get('student_id'),
                semester=form.cleaned_data.get('semester'),
                cgpa=form.cleaned_data.get('cgpa'),
                sgpa=form.cleaned_data.get('sgpa', 0.00),
                email=user.email,
                phone=form.cleaned_data.get('phone', ''),
                image=form.cleaned_data.get('image')
            )
            return redirect('student_login')
    else:
        form = StudentSignUpForm()
    return render(request, 'dashboard/student_signup.html', {'form': form})


def student_logout_view(request):
    if 'logged_student_id' in request.session:
        del request.session['logged_student_id']
    
    is_admin = request.user.is_superuser
    logout(request)
    
    if is_admin:
        return redirect('admin_login')
    return redirect('student_login')


@login_required(login_url='admin_login')
def delete_student_view(request, pk):
    # ব্যাকএন্ড সিকিউরিটি: সাধারণ স্টুডেন্ট যদি কোনোভাবে ইউআরএল দিয়েও ডিলিট করতে চায়, তা ব্লক হয়ে যাবে
    if not request.user.is_superuser:
        return redirect('student_portal')
        
    if request.user.is_superuser:
        try:
            student = Student.objects.get(pk=pk)
            student.delete()
        except Student.DoesNotExist:
            pass
    return redirect('dashboard')