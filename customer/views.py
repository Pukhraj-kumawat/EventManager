from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from .forms import VenueForm
from .models import Booking
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from EventPlanner.models import UserProfile,Category,Event,Venue
from EventPlanner.forms import SignUpForm
from django.db.models import Q


# Create your views here.

def book(request,pk):    
    category = Category.objects.get(id = pk)
    events = Event.objects.filter(category = category)    
    venues = Venue.objects.filter(category = category)

    venue_cities = [venue.city for venue in venues]
    unique_venue_cities = list(set(venue_cities))

    venue_names = [venue.name for venue in venues]
    unique_venue_names = list(set(venue_names))

    venue_min_prices = [venue.min_price for venue in venues]
    unique_venue_min_prices = list(set(venue_min_prices))  
  
    vendor_cities = [event.event_planner.userprofile.city for event in events]
    unique_vendor_cities = list(set(vendor_cities))

    vendor_names = {event.event_planner.first_name:event.event_planner.last_name for event in events}
    unique_vendor_names = {}
    for first_name,last_name in vendor_names.items():
        if first_name in unique_vendor_names.keys():
            if last_name in unique_vendor_names.values():
                pass
        else:
            unique_vendor_names[first_name] = last_name

    if request.method == 'GET':
        venue_city = request.GET.get('venue-city')
        venue_name = request.GET.get('venue-name')
        venue_min_price = request.GET.get('venue-min_price')
        vendor_city = request.GET.get('vendor-city')
        vendor_name = request.GET.get('vendor-name')
        vendor_first_name = request.GET.get('vendor-first-name')
        vendor_last_name = request.GET.get('vendor-last-name')
        try:
            if venue_city:            
                venues = Venue.objects.filter(category = category,city__icontains = venue_city)                
            if venue_name:
                venues = Venue.objects.filter(category = category,name__icontains = venue_name)
            if venue_min_price:                
                venues = Venue.objects.filter(category = category,min_price__lte = float(venue_min_price))                                
            if vendor_city:
                userprofile_set = UserProfile.objects.filter(city__icontains = vendor_city)
                events = []
                for userprofile in userprofile_set:
                    events_list = Event.objects.filter(event_planner = userprofile.user,category = category)
                    for event in events_list:
                        events.append(event)
            if vendor_name:
                user_set = User.objects.filter( Q(first_name__icontains = vendor_name) | Q(last_name__icontains = vendor_name))
                events = []
                for user in user_set:
                    events_list = Event.objects.filter(event_planner = user,category = category)
                    for event in events_list:
                        events.append(event)
            if vendor_first_name and vendor_last_name:
                user_set = User.objects.filter(first_name = vendor_first_name,last_name = vendor_last_name)
                events = []
                for user in user_set:
                    events_list = Event.objects.filter(event_planner = user,category = category)
                    for event in events_list:
                        events.append(event)
        except:
            pass
    
    context = {'events':events,'venues':venues,'pk':pk,'unique_venue_cities':unique_venue_cities,'unique_venue_names':unique_venue_names,'unique_venue_min_prices':unique_venue_min_prices,'unique_vendor_cities':unique_vendor_cities,'unique_vendor_names':unique_vendor_names}

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
def create_book(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        if not time:
            time = '00:00:00'
        venue_id = request.POST.get('venue_id')
        vendor_id = request.POST.get('vendor_id')       
    if venue_id and vendor_id :
        venue = Venue.objects.get(id = venue_id)
        vendor = User.objects.get(id = vendor_id)
        booking = Booking(venue=venue,vendor=vendor,user = request.user,date=date,time=time)        
    if venue_id:
        venue = Venue.objects.get(id = venue_id)
        vendor = None
        booking = Booking(venue=venue,user = request.user,date=date,time=time)        
    if vendor_id:
        vendor = User.objects.get(id = vendor_id)
        venue = None
        booking = Booking(vendor=vendor,user = request.user,date=date,time=time)  
    booking.save()
    return redirect('/booked/')

@login_required(login_url='/login-C/')
def booked(request):  
    bookings = Booking.objects.all()
    context = {'bookings':bookings}
    return render(request,'customer/booked.html',context)

def delete_book(request):
    if request.method == 'POST':
        try:        
            booking_id = request.POST.get('booking_id')
            booking = Booking.objects.get(id=booking_id)
            booking.delete()      
        except:
            pass
    return redirect('/booked/')