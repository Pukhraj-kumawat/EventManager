from django.shortcuts import render
from EventPlanner.models import Category,Event,UserProfile
from django.contrib.auth.models import User

# Create your views here.

def book(request,pk):
    category = Category.objects.get(id=pk)
    events = Event.objects.filter(category=category)
    context = {'events':events}
    return render(request,'customer/booking.html',context)