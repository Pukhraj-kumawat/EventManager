from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from . import forms
from .models import Booking
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from EventPlanner.models import UserProfile,Category,Event,Venue
from EventPlanner.forms import SignUpForm

# Create your views here.

def book(request,pk):
    category = Category.objects.get(id=pk)
    events = Event.objects.filter(category=category)
    venues = Venue.objects.filter(category=category)
    context = {'events':events,'venues':venues}
    return render(request,'customer/booking.html',context)


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

def full_package(request,pk):
    venue = Venue.objects.get(id=pk)
    vendors = venue.vendors.all()
    vender_data = {}
    for vendor in vendors:
        vendor_profile = UserProfile.objects.get(user=vendor)
        vender_data[vendor] = vendor_profile 
    
    context = {'venue':venue,'vendors':vendors,'vender_data':vender_data}
    return render(request,'customer/full-package.html',context)

@login_required(login_url='/login-C/')
def create_book(request,venue_id=None,vendor_id = None):
    if venue_id and vendor_id :
        venue = Venue.objects.get(id = venue_id)
        vendor = User.objects.get(id = vendor_id)
        Booking.objects.create(venue=venue,vendor=vendor,user = request.user)
    elif venue_id:
        venue = Venue.objects.get(id = venue_id)
        vendor = None
        Booking.objects.create(venue=venue,user = request.user)
    else:
        vendor = User.objects.get(id = vendor_id)
        venue = None
        Booking.objects.create(vendor=vendor,user = request.user)
    return redirect('/booked/')

@login_required(login_url='/login-C/')
def booked(request):
    bookings = Booking.objects.all()
    context = {'bookings':bookings}
    return render(request,'customer/booked.html',context)