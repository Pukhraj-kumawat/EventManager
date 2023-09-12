from django.shortcuts import render,redirect,HttpResponse
from .models import Category,Event,UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from customer import views
from .forms import SignUpForm
import re



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
    validation_error = None
    if request.method == 'POST':
        try:
            # access filled form instance
            form = SignUpForm(request.POST)

            if form.is_valid():
                user = form.save(commit=False)
                # save the form 
                user.save()
                # create the UserProfile for the above user
                UserProfile_instance = UserProfile.objects.create(user=user,is_event_planner=True)
                # login the user
                login(request,user)
                # redirect the user to logged in page
                return redirect('/logged-in-E/')
            else:
                # catch the error
                validation_error = form.errors                
        except:
            pass
    context = {'signUpForm':SignUpForm,'validation_error':validation_error,}
    return render(request,'EventPlanner/sign-up.html',context)
    
@login_required(login_url='/login-E/')
def loggedIn(request):
    return render(request,'EventPlanner/logged-in.html')


def loginPage(request):
    validation_error = False
    if request.user.is_authenticated:
        return redirect('/logged-in-C/')
    if request.method == 'POST':
        try:
            # fetch the data from HTML login form
            username = request.POST.get('username')
            password = request.POST.get('password')
            # authenticate the user
            user = authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                return redirect('/logged-in-E/')
            else:
                validation_error = True
        except:
            pass
    context = {'validation_error':validation_error}
    return render(request,'EventPlanner/login-page.html',context)

                
def logoutPage(request):
    logout(request)
    return redirect('/login-E/')

