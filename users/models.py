from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
status = [('Individual', 'Individual'),
          ('Student', 'Student')]


class CustomUser(AbstractUser):
    signup_as = models.CharField(max_length=20,
                                 choices=status,
                                 default='Indvidual')
