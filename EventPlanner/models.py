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
    
user_type_choices = (('is_customer','is_customer'),('is_event_planner','is_event_planner'))

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    user_type = models.CharField(choices=user_type_choices,max_length=50)
    contact_info = models.CharField(max_length=200,blank=True,null=True,verbose_name='Contact information')
    company_name = models.CharField(max_length=50,blank=True,null=True)
    website = models.URLField(max_length=200,blank=True,null=True)
    bio = models.TextField(blank=True,null=True)
    city = models.CharField(max_length=20,null=False,blank=False)
    location = models.TextField(blank=True,null=True)
    service_offered = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.user.username

venue_choices = (('Rajasthan','Rajasthan'),('Gujrat','Gujrat'),('Madhya pradesh','Madhya pradesh'),('Maharastra','Maharastra'))

class Venue(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False)
    min_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    location = models.TextField(null=False,blank=False)
    city = models.CharField(max_length=20,null=False,blank=False)
    state = models.CharField(choices=venue_choices,max_length=50,null=False,blank=False)
    vendors = models.ManyToManyField(User,null=True,blank=True)
    category = models.ManyToManyField(Category)
    service_offered = models.TextField(null=True,blank=True)

    
