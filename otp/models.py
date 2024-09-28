from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'age', 'gender']

    def __str__(self):
        return self.email

import random
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'OTP for {self.user.email}'

    def send_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.save()
        # Here, integrate your OTP sending logic (Email/SMS)
        send_mail(
            'Your OTP Code',
            f'Your OTP is {self.otp}',
            settings.EMAIL_HOST_USER,
            [self.user.email],
            fail_silently=False,
        )
