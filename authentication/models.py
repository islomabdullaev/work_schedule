from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    username = models.CharField(max_length=128, unique=True)
    position = models.CharField(max_length=128)
    date_of_birth = models.DateTimeField()
