from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from . import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from EventPlanner.models import UserProfile,Category,Event
from EventPlanner.forms import SignUpForm

# Create your views here.

def book(request,pk):
    category = Category.objects.get(id=pk)
    events = Event.objects.filter(category=category)
    context = {'events':events}
    return render(request,'customer/booking.html',context)

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
                UserProfile_instance = UserProfile.objects.create(user=user,is_customer=True)
                login(request,user)
                # redirect the user to logged in page
                return redirect('/logged-in-C/')                
            else:
                validation_error = form.errors
        except:
            pass    
    context = {'signUpForm':SignUpForm,'validation_error':validation_error}
    return render(request,'customer/sign-up.html',context)


def loginPage(request):
    validation_error = False
    if request.user.is_authenticated:
        return redirect('/logged-in-C/')
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                return redirect('/logged-in-C/')
            else:
                validation_error = True
        except:
            pass
    context = {'validation_error':validation_error}
    return render(request,'customer/login-page.html',context)

@login_required(login_url='/login-C/')
def loggedIn(request):
    return render(request,'customer/logged-in.html')