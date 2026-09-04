from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=50, unique=True)
    semester = models.CharField(max_length=50)
    cgpa = models.DecimalField(max_digits=3, decimal_places=2)
    sgpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    email = models.EmailField(unique=True, default="student@example.com")
    phone = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(upload_to='student_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.student_id})"


class StudentOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.otp_code}"