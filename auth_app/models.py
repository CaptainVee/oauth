from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    REGISTRATION_CHOICES = [
        ('email', 'email'),
        ('google', 'google')
    ]
    email = models.CharField(max_length=250, unique=True, null=True, blank=True)
    registration_method = models.CharField(max_length=10, choices=REGISTRATION_CHOICES, default='email')

    def __str__(self) -> str:
        return self.username
