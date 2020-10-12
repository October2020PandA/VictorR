from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import datetime
from django.utils.dateparse import parse_date

class Users(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SchedulesManager(models.Manager):
    def schedule_val(self, postData):
        errors = {}
        if len(postData['date']) == 0:
            errors['date']="A Date is required"
        elif parse_date(postData['date']) < datetime.date.today():
            errors['date']="You must schedule in a future date"
        if len(postData['time_list']) == 0:
            errors['time_list']="A Time is required"
        if len(postData['desc']) == 0:
            errors['description']="A Description is required"
        elif len(postData['desc']) < 3:
            errors['description']="Your Description should be at least 3 characters"
        return errors

class Schedules(models.Model):
    description = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    scheduler = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="schedule", on_delete=models.CASCADE)
    confirm = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SchedulesManager()