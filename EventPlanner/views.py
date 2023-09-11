from django.shortcuts import render,redirect,HttpResponse
from .models import Category,Event,UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from customer import views
from .forms import SignUpForm


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
    if request.method == 'POST':
        try:
            form = SignUpForm(request.POST)
            form.save()
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                UserProfile_instance = UserProfile.objects.create(user=user,is_event_planner=True)
        except:
            pass    
    context = {'signUpForm':SignUpForm}
    return render(request,'EventPlanner/sign-up.html',context)
    
def loggedIn(request):
    return render(request,'EventPlanner/logged-in.html')

                
