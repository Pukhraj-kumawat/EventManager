from django.contrib import admin
from .models import Category,Event,UserProfile,Venue

# Register your models here.

admin.site.register(Event)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Venue)

