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
