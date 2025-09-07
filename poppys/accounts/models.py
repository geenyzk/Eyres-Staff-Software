from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# accounts/models.py

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    is_manager = models.BooleanField(default=False)

    def __str__(self):
        return self.username