from django.shortcuts import render,redirect,HttpResponse
from .models import Category,Event,UserProfile,Venue
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from customer import views
from .forms import SignUpForm,UserProfileForm,UserForm
from django.contrib.auth.forms import PasswordChangeForm
import re
from customer.forms import MessageForm
from customer.models import Messages
import uuid


# Create your views here.

def home(request):
    filter  = None
    categories = Category.objects.all()
    categories_list = []
    for category in categories:
        Events = Event.objects.filter(category = category)
        Venues = Venue.objects.filter(category = category)
        if Events and Venues:            
            categories_list.append(category)
            categories = categories_list
        elif Events and not Venues:            
            categories_list.append(category)
            categories = categories_list        
        elif not Events and Venues:            
            categories_list.append(category)
            categories = categories_list
        else:
            pass     
    users = User.objects.all()
    if request.method == 'GET':
        try:
            event = request.GET.get('event')
            if event:
                categories = Category.objects.filter(name__icontains = event)
                for category in categories:
                    categories_list.append(category)
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

def signUp(request,user_type):
    validation_error = None
    if request.method == 'POST':
        try:
            # access filled form instance
            form = SignUpForm(request.POST)

            if form.is_valid():
                user = form.save(commit=False)
                # save the form 
                user.save()
                # Check whther user is an event planner 
                if user_type == 'is_event_planner':
                # create the UserProfile for the above user
                    UserProfile_instance = UserProfile.objects.create(user=user,user_type='is_event_planner')
                    # login the user
                    login(request,user)
                    # redirect the user to logged in page
                    return redirect('/logged-in-E/')                    
                else:
                    UserProfile_instance = UserProfile.objects.create(user=user,user_type='is_customer')
                    # login the user
                    login(request,user)
                    # redirect the user to logged in page
                    return redirect('/logged-in-C/')      
            else:
                # catch the error
                validation_error = form.errors                
        except:
            pass
    context = {'signUpForm':SignUpForm,'validation_error':validation_error,'user_type':user_type}
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


@login_required(login_url='/login-E/')
def profile(request,pk):
    user_errors = None
    profile_errors = None
    user = User.objects.get(id=pk)
    user_profile = UserProfile.objects.get(user = user)
    profile_form = UserProfileForm(instance=user_profile,initial={'website': user_profile.website if user_profile.website else 'https://'})
    user_form = UserForm(instance = user)
    if request.method == 'POST':
        try:
            profile_form = UserProfileForm(request.POST,instance=user_profile)
            user_form = UserForm(request.POST,instance=user)
            if user_form.is_valid():
                user_form.save()
            else:
                user_errors = user_form.errors
            if profile_form.is_valid():
                form_data = profile_form.save(commit=False)
                form_data.user = request.user            
                form_data.save()
            else:
                profile_errors = profile_form.errors
        except:
            pass        
    context = {'UserProfileForm':profile_form,'user_errors':user_errors,'profile_errors':profile_errors,'user_form':user_form,'user_profile':user_profile}
    return render(request,'EventPlanner/profile.html',context)

@login_required(login_url='/login-E/')
def ChangePassword(request):
    errors = None
    password_form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        try:
            changed_password = PasswordChangeForm(request.user,request.POST)
            if changed_password.is_valid():
                changed_password.save()
            else:
                errors = changed_password.errors
        except:
            pass
    context = {'password_form':password_form,'errors':errors}
    return render(request,'EventPlanner/change-password.html',context)


def EventPlannerInfo(request,pk):      
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('/login-C/')
        unique_token_form = request.POST.get('unique-token')
        unique_token_session = request.session.get('chat_token')
        if unique_token_form == unique_token_session:
            message_form = MessageForm(request.POST)
            if message_form.is_valid():
                message_object = message_form.save(commit = False)
                message_object.sender = request.user
                vendor = User.objects.get(id=int(pk))
                message_object.receiver = vendor
                message_object.save()
                del request.session['chat_token']
                return redirect(f'/event-planner-info/{pk}/')            
    else:
        unique_token = str(uuid.uuid4())
        request.session['chat_token'] = unique_token        
    if request.user.is_authenticated:
        messages = Messages.objects.filter(sender = request.user)
    else:
        messages = None
    vendor = User.objects.get(id = pk)
    user_profile = UserProfile.objects.get(user = vendor)
    user_profile_form = UserProfileForm(instance = user_profile)
    
    context = {'user_profile_form':user_profile_form,'vendor':vendor,'MessageForm':MessageForm,'messages':messages,'unique_token':unique_token,'pk':pk,}    

    return render(request,'EventPlanner/event-planner-info.html',context)

def VenueInfo(request,pk):
    return render(request,'EventPlanner/venue-info.html')

def DeleteAccount(request):
    return render(request,'EventPlanner/delete-account.html')

def confirmDelete(request):
    user = request.user
    user.delete()
    return redirect('/')