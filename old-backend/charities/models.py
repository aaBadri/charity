from django.db import models
from django.db.models import Q
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


class TaskManager(models.Manager):
    def related_tasks_to_charity(self, user):
        return (
            super()
            .get_queryset()
            .filter(charity__isnull=False)
            .filter(charity__user=user)
        )

    def related_tasks_to_benefactor(self, user):
        return (
            super()
            .get_queryset()
            .filter(assigned_benefactor__isnull=False)
            .filter(assigned_benefactor__user=user)
        )

    def all_related_tasks_to_user(self, user):
        return (
            super()
            .get_queryset()
            .filter(
                Q(Q(charity__user=user) & Q(charity__isnull=False))
                | Q(
                    Q(assigned_benefactor__user=user)
                    & Q(assigned_benefactor__isnull=False)
                )
                | Q(state="P")
            )
        )


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
    charity = models.ForeignKey(Charity, on_delete=models.SET_NULL, null=True)
    age_limit_from = models.IntegerField(blank=True, null=True)
    age_limit_to = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    gender_limit = models.CharField(
        max_length=1, choices=GENEDER_CHOICES, blank=True, null=True
    )
    state = models.CharField(max_length=1, choices=STATE_CHOICES, default=PENDING)
    title = models.CharField(max_length=60)
    objects = TaskManager()
