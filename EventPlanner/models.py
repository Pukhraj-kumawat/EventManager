from django.db import models
from django.contrib.auth.models import User
# from phonenumber_field.formfields import PhoneNumberField

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
    
CHOICES = (('is_customer','is_customer'),('is_event_planner','is_event_planner'))

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    user_type = models.CharField(choices=CHOICES,max_length=50)
    contact_info = models.CharField(max_length=200,blank=True,null=True)
    company_name = models.CharField(max_length=50,blank=True,null=True)
    website = models.URLField(max_length=200,blank=True,null=True)
    bio = models.TextField(blank=True,null=True)
    location = models.TextField(blank=True,null=True)
    service_offered = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.user.username



    
