from django.contrib import admin
from .models import Category,Event,UserProfile,Venue,Image

# Register your models here.

class customUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_type','otp_verified')


admin.site.register(Event)
admin.site.register(Category)
admin.site.register(UserProfile,customUserAdmin)
admin.site.register(Venue)
admin.site.register(Image)
