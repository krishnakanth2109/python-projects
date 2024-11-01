from django.db import models

# Create your models here.
# users/models.py
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=[('USER', 'User'), ('ADMIN', 'Admin')])

    def __str__(self):
        return self.username
