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

def home(request):
    if not request.user.is_authenticated or request.user.userprofile.user_type == 'is_customer':
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
        return render(request,'customer/home.html',context)


def book(request,pk):
    if not request.user.is_authenticated or request.user.userprofile.user_type == 'is_customer':        
        error = None
        category = Category.objects.get(id = pk)
        events = Event.objects.filter(category = category)    
        venues = Venue.objects.filter(category = category)

        if request.method == 'GET':
            venue_city = request.GET.get('venue-city')
            min_price = request.GET.get('min_price')
            max_price = request.GET.get('max_price')
            vendor_city = request.GET.get('vendor-city')
            vendor_name = request.GET.get('vendor-name')
            vendor_first_name = request.GET.get('vendor-first-name')
            vendor_last_name = request.GET.get('vendor-last-name')
            try:
                if venue_city and not min_price:            
                    venues = Venue.objects.filter(category = category,city__icontains = venue_city)    
                                                    
                if min_price and max_price and not venue_city:
                    venues = Venue.objects.filter(category = category,min_price__lt = float(max_price),min_price__gte = float(min_price))
                    
                if min_price and max_price and venue_city:
                    venues = Venue.objects.filter(category=category,city__icontains = venue_city,min_price__lt = float(max_price),min_price__gte = float(min_price))

                if vendor_city:
                    userprofile_set = UserProfile.objects.filter(city__icontains = vendor_city)
                    if not userprofile_set:
                        vendor_city = 'unavailable'
                    events = []
                    for userprofile in userprofile_set:
                        events_list = Event.objects.filter(event_planner = userprofile.user,category = category)
                        for event in events_list:
                            events.append(event)

                    null_events = Event.objects.filter(category = category)            
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
        
        context = {'error':error,'events':events,'venues':venues,'pk':pk,'venue_city':venue_city,'min_price':min_price,'max_price':max_price,'vendor_city':vendor_city,}

        return render(request,'customer/booking.html',context)


def loginPage(request):
    validation_error = False
    if request.user.is_authenticated:
        return redirect('/home-C/')
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username=username,password=password)
            if user:
                if user.userprofile.user_type == 'is_customer':                
                    login(request,user)
                    return redirect('/home-C/')
                else:
                    validation_error = True
            else:
                validation_error = True
        except:
            pass
    context = {'validation_error':validation_error}
    return render(request,'customer/login-page.html',context)

# @login_required(login_url='/login-C/')
# def loggedIn(request):
#     return render(request,'customer/logged-in.html')

def full_package(request,pk):
    if not request.user.is_authenticated or request.user.userprofile.user_type == 'is_customer':
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
    if request.user.userprofile.user_type == 'is_customer':
        if request.method == 'POST':
            date = request.POST.get('date')
            time = request.POST.get('time')
            location = request.POST.get('location')
            if not time:
                time = '00:00:00'
            venue_id = request.POST.get('venue_id')
            vendor_id = request.POST.get('vendor_id')       
        if venue_id and vendor_id :
            venue = Venue.objects.get(id = venue_id)
            vendor = User.objects.get(id = vendor_id)
            booking = Booking(venue=venue,vendor=vendor,user = request.user,date=date,time=time,location = location)        
        if venue_id and not vendor_id:
            venue = Venue.objects.get(id = venue_id)
            vendor = None
            booking = Booking(venue=venue,user = request.user,date=date,time=time,location = location)        
        if vendor_id and not venue_id:
            vendor = User.objects.get(id = vendor_id)
            venue = None
            booking = Booking(vendor=vendor,user = request.user,date=date,time=time,location = location)  
        booking.save()
        return redirect('/booked/')

@login_required(login_url='/login-C/')
def booked(request):  
    if request.user.userprofile.user_type == 'is_customer':
        bookings = Booking.objects.all()
        context = {'bookings':bookings}
        return render(request,'customer/booked.html',context)

@login_required(login_url='/login-C/')
def delete_book(request):
    if request.user.userprofile.user_type == 'is_customer':
        if request.method == 'POST':
            try:        
                booking_id = request.POST.get('booking_id')
                booking = Booking.objects.get(id=booking_id)
                booking.delete()      
            except:
                pass
        return redirect('/booked/')

