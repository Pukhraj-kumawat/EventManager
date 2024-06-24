from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.db import models

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

    def __str__(self):
        return self.name
    
user_type_choices = (('is_customer','is_customer'),('is_event_planner','is_event_planner'))

class Image(models.Model):
    user_profile = models.ForeignKey('userprofile',on_delete = models.CASCADE,null = True,blank = True)
    venue_object = models.ForeignKey('Venue',on_delete = models.CASCADE,null = True, blank = True)
    # image = models.ImageField(upload_to='images/',null = True,blank = True)
    image = CloudinaryField('image',blank=True,null=True)
    upload_date = models.DateTimeField(auto_now = True)

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    user_type = models.CharField(choices=user_type_choices,max_length=50)
    contact_info = models.CharField(max_length = 200,blank = True,null = True,verbose_name='Contact information')
    company_name = models.CharField(max_length =  50,blank = True,null = True)
    website = models.URLField(max_length = 200,blank = True,null = True)
    about = models.TextField(blank = True,null = True)
    city = models.CharField(max_length = 20,null = False,blank = False)
    state = models.CharField(max_length = 20,null = False,blank = False)
    location = models.TextField(blank = True,null = True)
    service_offered = models.TextField(blank = True,null = True)
    profile_picture = CloudinaryField('image',blank=True,null=True)
    vendor_images = models.ManyToManyField('Image', blank = True,null = True,related_name = 'portfolio_images')
    otp_verified = models.BooleanField(default=False)
    # showcase_image = models.OneToOneField('Image',blank = True,null = True,on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username

venue_choices = (('Rajasthan','Rajasthan'),('Gujrat','Gujrat'),('Madhya pradesh','Madhya pradesh'),('Maharastra','Maharastra'))

class Venue(models.Model):
    name = models.CharField(max_length=100,null = False,blank = False)
    about = models.TextField(blank = True,null = True)
    min_price = models.DecimalField(max_digits = 10, decimal_places = 2,null = True,blank = True)
    max_capacity = models.IntegerField(null = False,blank = False)
    location = models.TextField(null = False,blank = False)
    city = models.CharField(max_length = 20,null = False,blank = False)
    state = models.CharField(choices = venue_choices,max_length = 50,null = False,blank = False)
    vendors = models.ManyToManyField(User,null = True,blank = True)
    category = models.ManyToManyField(Category)
    service_offered = models.TextField(null = True,blank = True)
    contact_info = models.TextField(null = False,blank = False)
    venue_images = models.ManyToManyField('Image', blank = True,null = True)

    

# accounts/models.py


