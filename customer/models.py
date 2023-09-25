from django.db import models
from django.contrib.auth.models import User
from EventPlanner.models import Venue


# Create your models here.

class Booking(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='booking_user',null=False)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE,null=True)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    location = models.CharField(max_length=150,null=True,blank=True)

class Messages(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False,related_name = 'receiver')
    message = models.TextField(null=False,blank=False)
    created=models.DateTimeField(auto_now_add = True)

