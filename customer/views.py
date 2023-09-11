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


def loginPage(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                return redirect('/logged-in-C/')
            else:
                return HttpResponse("Not authenticated")
        except:
            pass
    context = {}
    return render(request,'customer/login-page.html',context)

@login_required(login_url='/login-C/')
def loggedIn(request):
    return render(request,'customer/logged-in.html')