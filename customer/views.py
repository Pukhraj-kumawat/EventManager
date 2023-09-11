from django.shortcuts import render
from django.contrib.auth.models import User
from . import forms
from django.contrib.auth.forms import UserCreationForm
from EventPlanner.models import UserProfile,Category,Event
from EventPlanner.forms import SignUpForm

# Create your views here.

def book(request,pk):
    category = Category.objects.get(id=pk)
    events = Event.objects.filter(category=category)
    context = {'events':events}
    return render(request,'customer/booking.html',context)

def signUp(request):
    if request.method == 'POST':
        try:
            form = SignUpForm(request.POST)
            form.save()
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                UserProfile_instance = UserProfile.objects.create(user=user,is_customer=True)
        except:
            pass    
    context = {'signUpForm':SignUpForm}
    return render(request,'customer/sign-up.html',context)


def loggedIn(request):
    return render(request,'customer/logged-in.html')