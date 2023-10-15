from django.shortcuts import render,redirect,HttpResponse
from .models import Category,Event,UserProfile,Venue,Image
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from customer import views
from .forms import SignUpForm,UserProfileForm,UserForm,VenueForm,EventForm,ImageForm
from django.contrib.auth.forms import PasswordChangeForm
import re
from customer.forms import MessageForm
from customer.models import Messages,Booking
import uuid
from django.db import connection
import os
from django.core.files import File
import boto3



# Create your views here. yes ok

#hello

@login_required(login_url='/login/')
def home(request):    
    if request.user.userprofile.user_type == 'is_event_planner':
        # if request.method =='POST':
        #     message = request.POST.get('message')
        #     receiver = request.POST.get('receiver')    
        #     receiver_instance = User.objects.get(username = receiver)
        #     Messages.objects.create(sender = request.user,receiver = receiver_instance, message =  message)            

        bookings = Booking.objects.filter(vendor = request.user)
        events = Event.objects.filter(event_planner = request.user)
        
        try:
            received_dict,sent_dict = Messages_display(request)
        except:
            received_dict = None
            sent_dict = None

        context = {'bookings':bookings,'received_dict':received_dict,'sent_dict':sent_dict,'MessageForm':MessageForm,'events':events}

        return render(request,'EventPlanner/home.html',context)


def create_messages(request):
    if request.method =='POST':
            message = request.POST.get('message')
            receiver = request.POST.get('receiver')    
            receiver_instance = User.objects.get(username = receiver)
            Messages.objects.create(sender = request.user,receiver = receiver_instance, message =  message)  
    return redirect('/home-E/')


# def planner(request):
#     return render(request,'EventPlanner/planner.html')

# def book(request,pk):
#     category = Category.objects.get(id=pk)
#     events = Event.objects.filter(category=category)
#     context = {'events':events}
#     return render(request,'EventPlanner/booking.html',context)

def signUp(request,user_type):
    if not request.user.is_authenticated:
        validation_error = None
        if request.method == 'POST':
            try:
                # access filled form instance
                form = SignUpForm(request.POST)

                if form.is_valid():
                    user = form.save(commit = False)
                    # save the form 
                    user.save()
                    # Check whther user is an event planner 
                    if user_type == 'is_event_planner':
                    # create the UserProfile for the above user ohk
                    
                        UserProfile_instance = UserProfile.objects.create(user=user,user_type='is_event_planner')
                        # login the user
                        login(request,user)
                        # redirect the user to home in page
                        return redirect('/home-E/')                    
                    else:
                        UserProfile_instance = UserProfile.objects.create(user=user,user_type='is_customer')
                        # login the user
                        login(request,user)
                        # redirect the user to logged in helo hello
                        return redirect('/home-C/')      
                else:
                    # catch the error
                    validation_error = form.errors                
            except:                
                pass
        context = {'signUpForm':SignUpForm,'validation_error':validation_error,'user_type':user_type}
        return render(request,'EventPlanner/sign-up.html',context)



def loginPage(request):
    if not request.user.is_authenticated:
        validation_error = False
        if request.user.is_authenticated:
            return redirect('/home-E/')
        if request.method == 'POST':
            try:
                # fetch the data from HTML login form
                username = request.POST.get('username')
                password = request.POST.get('password')
                # authenticate the user
                user = authenticate(request,username = username,password = password)                
                if user:
                    if user.userprofile.user_type == 'is_event_planner':
                        login(request,user)
                        return redirect('/home-E/')
                    if user.userprofile.user_type == 'is_customer':                        
                        login(request,user)                        
                        return redirect('/home-C')
                else:
                    validation_error = True
            except:
                pass
        context = {'validation_error':validation_error}
        return render(request,'EventPlanner/login-page.html',context)

@login_required(login_url='/login/')                
def logoutPage(request):
    logout(request)
    return redirect('/login/')


@login_required(login_url='/login/')
def edit_profile(request):    
    user_errors = None
    profile_errors = None    
    button_clicked = None
    user_profile = UserProfile.objects.get(user = request.user)
    profile_form = UserProfileForm(instance = user_profile,initial={'website': user_profile.website if user_profile.website else 'https://'})
    user_form = UserForm(instance = request.user)            
    if request.method == 'POST':                                                   
        # try:                        
        profile_form = UserProfileForm(request.POST,request.FILES,instance = user_profile)                   
        user_form = UserForm(request.POST,instance = request.user)
        button_clicked = request.POST.get('button-clicked')                           
        if button_clicked:                                                   
            # default_profile = open('media/images/No profile.jpeg','rb')                
            url_s3 = request.user.userprofile.profile_picture.url.split('?')[0]
            s3_client = boto3.client("s3")
            response = s3_client.delete_object(Bucket ='eventmanagementbucket', Key = url_s3)
            request.user.userprofile.profile_picture.delete()                                                
            # request.user.userprofile.profile_picture.save('default_profile',File(default_profile))            
            # default_profile.close()
            return redirect('/profile/')                  
        if user_form.is_valid():                             
            user_form.save()
            if request.user.userprofile.user_type =='is_customer':
                return redirect('/profile/')                                     
        else:
            user_errors = user_form.errors            
                    
        if profile_form.is_valid():                
            changed_fields = profile_form.changed_data 
            if 'profile_picture' in changed_fields:                    
                if request.user.userprofile.profile_picture:                                        
                    request.user.userprofile.profile_picture.delete()                        

            form_data = profile_form.save(commit = False)                
            form_data.user = request.user            
            form_data.save()
            return redirect('/profile/')
        else:
            profile_errors = profile_form.errors
        # except Exception as e:             
        #     pass        
    context = {'UserProfileForm':profile_form,'user_errors':user_errors,'profile_errors':profile_errors,'user_form':user_form,'user_profile':user_profile,'button_clicked':button_clicked}
    return render(request,'EventPlanner/edit-profile.html',context)

@login_required(login_url='/login/')
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
    if not request.user.is_authenticated or request.user.userprofile.user_type == 'is_customer':
        user = User.objects.get(id = int(pk))
        user_profile = UserProfile.objects.get(user = user)
        images = Image.objects.filter(user_profile = user_profile)  
        if request.method == 'POST':
            if not request.user.is_authenticated:
                return redirect('/login/')
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
        try:
            received_dict,sent_dict = Messages_display(request)
        except:
            received_dict = None
            sent_dict = None
        context = {'user_profile_form':user_profile_form,'vendor':vendor,'MessageForm':MessageForm,'messages':messages,'unique_token':unique_token,'pk':pk,'received_dict':received_dict,'sent_dict':sent_dict,'images':images}    

        return render(request,'EventPlanner/event-planner-info.html',context)

def VenueInfo(request,pk):
    if not request.user.is_authenticated or request.user.userprofile.user_type == 'is_customer':
        venue = Venue.objects.get(id = pk)
        images = Image.objects.filter(venue_object = venue)
        venue_form = VenueForm(instance = venue)
        context = {'venue_form':venue_form,'images':images}
        return render(request,'EventPlanner/venue-info.html',context)

@login_required(login_url='/login/')
def DeleteAccount(request):
    return render(request,'EventPlanner/delete-account.html')

@login_required(login_url='/login/')
def confirmDelete(request):
    user = request.user
    user.delete()
    return redirect('/home-C/')

@login_required(login_url='/login/')
def Messages_display(request):
        messages_as_receiver = Messages.objects.filter(receiver = request.user).order_by('sender')
        sender_list = []
        for message in messages_as_receiver:
            sender_list.append(message.sender)    
        sender_set = set(sender_list)

        message_as_sender = Messages.objects.filter(sender = request.user).order_by('receiver')
        receiver_list = []
        for message in message_as_sender:
            receiver_list.append(message.receiver)
        receiver_set = set(receiver_list)

        received_dict = {}
        sent_dict = {}

        for sender_of_set in sender_set:
            list_messages = []
            for message_received in messages_as_receiver:
                if sender_of_set == message_received.sender:
                    list_messages.append(message_received)
            received_dict[sender_of_set] = list_messages

        for receiver_of_set in receiver_set:
            list_messages = []
            for message_sent in message_as_sender:
                if receiver_of_set == message_sent.receiver:
                    list_messages.append(message_sent)
            sent_dict[receiver_of_set] = list_messages
        # if not received_dict:
        #     received_dict = None
        # if not sent_dict:
        #     sent_dict = None
            
        return received_dict,sent_dict

@login_required(login_url='/login/')
def profile(request):    
    user_profile = UserProfile.objects.get(user = request.user)
    userprofile_form = UserProfileForm(instance = user_profile)
    images = Image.objects.filter(user_profile = request.user.userprofile)
    context = {'user_profile':user_profile,'userprofile_form':userprofile_form,'images':images}
    return render(request,'EventPlanner/profile.html',context)

@login_required(login_url='/login/')
def create_event(request):
    if request.user.userprofile.user_type == 'is_event_planner':
        if request.method == 'POST':
            event_form = EventForm(request.POST)
            if event_form.is_valid():
                event_form_instance = event_form.save(commit = False)
                event_form_instance.event_planner = request.user
                event_form_instance.save()
                return redirect('/home-E/')
        context = {'EventForm':EventForm}
        return render(request,'EventPlanner/create-event.html',context)

@login_required(login_url='/login/')
def accept_booking(request,pk,status):
    if request.user.userprofile.user_type == 'is_event_planner':
        booking_object  = Booking.objects.get(id = int(pk))
        if status == 'accepted':
            booking_object.booking_accepted = True
            booking_object.save()            
        else:
            booking_object.booking_accepted = False
            booking_object.save()            
        return redirect('/home-E/')


@login_required(login_url='/login/')
def edit_event(request,pk):
    if request.user.userprofile.user_type == 'is_event_planner':
        event = Event.objects.get(id = int(pk))
        event_form = EventForm(instance = event)

        if request.method == 'POST':
            event_form_instance = EventForm(request.POST,instance = event)
            if event_form_instance.is_valid():
                event_form_instance.save()
                return redirect('/home-E/')
        context = {'event_form':event_form,}
        return render(request,'EventPlanner/edit-event.html',context)


@login_required(login_url='/login/')
def delete_event(request,pk):
    if request.user.userprofile.user_type == 'is_event_planner':
        event = Event.objects.get(id = int(pk))
        event.delete()
        return redirect('/home-E/')

@login_required(login_url='/login/')
def vendor_images(request):
    if request.user.userprofile.user_type == 'is_event_planner':
        images = Image.objects.filter(user_profile = request.user.userprofile)
        if request.method == 'POST':
            image_form = ImageForm(request.POST,request.FILES)
            if image_form.is_valid():
                image_form_instance = image_form.save(commit = False)
                image_form_instance.user_profile = request.user.userprofile
                if image_form_instance.image:                                
                    image_form_instance.save()
                    request.user.userprofile.vendor_images.add(image_form_instance)                                    
                    return redirect('/vendor-images/')
                                
            delete_image_id = request.POST.get('delete-image-id')              
            if delete_image_id:                                 
                image_to_delete  = Image.objects.get(id = int(delete_image_id)) 
                if image_to_delete:                                                           
                    image_to_delete.delete()
                    # remove image from media folder too.
                    if os.path.isfile(image_to_delete.image.path):
                        os.remove(image_to_delete.image.path)                                                     
                    return redirect('/vendor-images/')                
            return redirect('/vendor-images/')    
        context = {'ImageForm':ImageForm,'images':images,}
        return render(request, 'EventPlanner/vendor-images.html',context)


def hello():
    print('this is a sample function for resolving repo confilict')
    print('this is a new changes')