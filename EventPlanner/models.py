from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Event(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    event_planner = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    event_date_time = models.DateTimeField(null=True,blank=True)
    location = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
        return self.name
    

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    is_customer = models.BooleanField(default=False)
    is_event_planner = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username



    
