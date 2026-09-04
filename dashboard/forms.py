from django import forms
from django.contrib.auth.models import User
from .models import Student

class StudentLoginForm(forms.Form):
    student_id = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 text-white rounded-xl focus:outline-none focus:border-indigo-500 text-sm font-semibold',
            'placeholder': 'Enter your Student ID or type admin'
        })
    )

class AdminLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 text-white rounded-xl focus:outline-none focus:border-indigo-500 text-sm font-semibold',
            'placeholder': 'Enter Admin Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 text-white rounded-xl focus:outline-none focus:border-indigo-500 text-sm font-semibold',
            'placeholder': 'Enter Admin Password'
        })
    )

class StudentOTPVerifyForm(forms.Form):
    otp_code = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 text-white rounded-xl focus:outline-none focus:border-indigo-500 text-center tracking-widest text-xl font-bold',
            'placeholder': '••••••'
        })
    )

class StudentSignUpForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 text-white rounded-xl focus:outline-none focus:border-indigo-500 text-sm font-semibold',
            'placeholder': 'Enter Password'
        })
    )
    student_id = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 text-white rounded-xl focus:outline-none focus:border-indigo-500 text-sm font-semibold',
            'placeholder': 'Enter Student ID'
        })
    )
    semester = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 text-white rounded-xl focus:outline-none focus:border-indigo-500 text-sm font-semibold',
            'placeholder': 'e.g. Fall 2026'
        })
    )
    cgpa = forms.DecimalField(
        max_digits=3, decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 text-white rounded-xl focus:outline-none focus:border-indigo-500 text-sm font-semibold',
            'placeholder': 'e.g. 3.75'
        })
    )
    sgpa = forms.DecimalField(
        max_digits=3, decimal_places=2, required=False,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 text-white rounded-xl focus:outline-none focus:border-indigo-500 text-sm font-semibold',
            'placeholder': 'e.g. 3.80'
        })
    )
    phone = forms.CharField(
        max_length=20, required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 text-white rounded-xl focus:outline-none focus:border-indigo-500 text-sm font-semibold',
            'placeholder': 'Phone Number'
        })
    )
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 text-white rounded-xl focus:outline-none focus:border-indigo-500 text-sm font-semibold'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 text-white rounded-xl focus:outline-none focus:border-indigo-500 text-sm font-semibold',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 text-white rounded-xl focus:outline-none focus:border-indigo-500 text-sm font-semibold',
                'placeholder': 'Email Address'
            }),
        }

class AdminAddStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'name', 'semester', 'cgpa', 'sgpa', 'email', 'phone', 'image']
        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 bg-white border border-gray-300 rounded-xl text-xs sm:text-sm font-medium text-slate-900 focus:outline-none focus:border-indigo-600', 'placeholder': 'Student ID'}),
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 bg-white border border-gray-300 rounded-xl text-xs sm:text-sm font-medium text-slate-900 focus:outline-none focus:border-indigo-600', 'placeholder': 'Full Name'}),
            'semester': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 bg-white border border-gray-300 rounded-xl text-xs sm:text-sm font-medium text-slate-900 focus:outline-none focus:border-indigo-600', 'placeholder': 'Semester'}),
            'cgpa': forms.NumberInput(attrs={'class': 'w-full px-4 py-2.5 bg-white border border-gray-300 rounded-xl text-xs sm:text-sm font-medium text-slate-900 focus:outline-none focus:border-indigo-600', 'placeholder': 'CGPA'}),
            'sgpa': forms.NumberInput(attrs={'class': 'w-full px-4 py-2.5 bg-white border border-gray-300 rounded-xl text-xs sm:text-sm font-medium text-slate-900 focus:outline-none focus:border-indigo-600', 'placeholder': 'SGPA'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2.5 bg-white border border-gray-300 rounded-xl text-xs sm:text-sm font-medium text-slate-900 focus:outline-none focus:border-indigo-600', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 bg-white border border-gray-300 rounded-xl text-xs sm:text-sm font-medium text-slate-900 focus:outline-none focus:border-indigo-600', 'placeholder': 'Phone Number'}),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full px-3 py-2 bg-white border border-gray-300 rounded-xl text-xs font-medium text-slate-700'}),
        }