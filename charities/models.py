from django.db import models

from accounts.models import User


class Benefactor(models.Model):
    EXPERIENCE_CHOICES = ((0, "Junior"), (1, "Mid"), (2, "Senior"))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience = models.SmallIntegerField(choices=EXPERIENCE_CHOICES, default=0)
    free_time_per_week = models.PositiveSmallIntegerField(default=0)


class Charity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    reg_number = models.CharField(max_length=10)


class Task(models.Model):
    GENEDER_CHOICES = (("M", "Male"), ("F", "Female"))
    PENDING = "P"
    STATE_CHOICES = (
        (PENDING, "Pending"),
        ("W", "Waiting"),
        ("A", "Assigned"),
        ("D", "Done"),
    )

    assigned_benefactor = models.ForeignKey(
        Benefactor, on_delete=models.SET_NULL, null=True
    )
    charity = models.ForeignKey(Charity, on_delete=models.SET_NULL, null=True),
    age_limit_from = models.IntegerField(blank=True, null=True)
    age_limit_to = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    gender_limit = models.CharField(
        max_length=1, choices=GENEDER_CHOICES, blank=True, null=True
    )
    state = models.CharField(max_length=1, choices=STATE_CHOICES, default=PENDING)
    title = models.CharField(max_length=60)
