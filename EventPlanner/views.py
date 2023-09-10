from django.shortcuts import render
from .models import Category,Event,UserProfile
from django.contrib.auth.models import User
from . import forms


# Create your views here.

def home(request):
    filter  = None
    categories = Category.objects.all()
    users = User.objects.all()
    if request.method == 'GET':
        try:
            event = request.GET.get('event')
            if event:
                categories = Category.objects.filter(name__icontains=event)
                filter = 'Exists'
        except:
            pass
    context = {'categories':categories,'users':users,'filter':filter}    
    return render(request,'home.html',context)

def planner(request):
    return render(request,'EventPlanner/planner.html')

def book(request,pk):
    category = Category.objects.get(id=pk)
    events = Event.objects.filter(category=category)
    context = {'events':events}
    return render(request,'EventPlanner/booking.html',context)

def signUp(request):
    context = {'signUpForm':forms.SignUpForm}
    if request.method == 'POST':
        try:
            # create instance of filled form
            form = forms.SignUpForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                form.save()
            # fetch the above created user
            user = User.objects.get(username=username)
            # create userProfile for this user
            UserProfile.objects.create(user=user,is_event_planner=True)            
        except:
            pass
    return render(request,'EventPlanner/sign-up.html',context)
    