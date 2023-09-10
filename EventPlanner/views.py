from django.shortcuts import render
from .models import Category,Event,UserProfile
from django.contrib.auth.models import User


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

def createUser(request):
    context = {}
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            # create an event planner user
            User.objects.create(username=username,password=password)
            # fetch the above user
            user = User.objects.get(username=username)
            # create userProfile for this user
            UserProfile.objects.create(user=user,is_event_planner=True)
            
            User_profile = UserProfile.objects.get(user=user)

            context={'User_profile':User_profile}
        except:
            context={'error':'error'}
    return render(request,'EventPlanner/create-user.html',context)
    