from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    GENEDER_CHOICES = (("M", "Male"), ("F", "Female"))
    address = models.TextField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    gender = models.CharField(
        max_length=1, choices=GENEDER_CHOICES, blank=True, null=True
    )
    phone = models.CharField(max_length=15, null=True, blank=True)
