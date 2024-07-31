from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.

class User(AbstractUser):
    role_choices = (
        ("admin","Admin"),
        ("manager","Manageer"),
        ("member","Member"),
    )
    role = models.CharField(max_length=10, choices=role_choices)
    
    def save(self, *args, **kwargs):
        self.set_password(self.password)
        super().save(*args, **kwargs)