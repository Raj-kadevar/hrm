from django.contrib.auth.models import AbstractUser
from django.db.models import ImageField
from django.db import models
from .choices import LEAVE_CHOICES


class User(AbstractUser):
    profile = ImageField(blank=True, null=True, upload_to="profile/")
    manager = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    casual_leave = models.PositiveSmallIntegerField(default=1)
    emergency_leave = models.PositiveSmallIntegerField(default=5)
    device = models.TextField(null=True, blank=True)
class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    in_time = models.TimeField()
    out_time = models.TimeField()
    date = models.DateField()
    total_duration = models.TimeField()
    early_going	= models.TimeField()


class LeaveStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    leave_type = models.CharField(choices=LEAVE_CHOICES)
    leave_start_date = models.DateField()
    leave_end_date = models.DateField()


class Holiday(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.CharField(choices=LEAVE_CHOICES)
    leave_start_date = models.DateField()
    leave_end_date = models.DateField()
    reason = models.TextField()


class Device(models.Model):
    name = models.CharField()


class SelectedDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)