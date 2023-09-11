from django.shortcuts import render,redirect,HttpResponse
from .models import Category,Event,UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
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
    
@login_required(login_url='/login-E/')
def loggedIn(request):
    return render(request,'EventPlanner/logged-in.html')


def loginPage(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                return redirect('/logged-in-E/')
            else:
                return HttpResponse("Not authenticated")
        except:
            pass
    context = {}
    return render(request,'EventPlanner/login-page.html',context)

                
def logoutPage(request):
    logout(request)
    return redirect('/login-E/')