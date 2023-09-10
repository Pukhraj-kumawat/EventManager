from django.shortcuts import render
from EventPlanner.models import UserProfile
from django.contrib.auth.models import User
from . import forms

# Create your views here.

def book(request,pk):
    category = Category.objects.get(id=pk)
    events = Event.objects.filter(category=category)
    context = {'events':events}
    return render(request,'customer/booking.html',context)

def signUp(request):
    context = {'signUpForm':forms.SignUpForm}
    if request.method == 'POST':
        try:
            form = forms.SignUpForm(request.POST)
            if form.is_valid():
                # fetch username from form
                username = form.cleaned_data['username']
                form.save()
            # fetch the above created user
            user = User.objects.get(username=username)
            # create UserProfile 
            UserProfile.objects.create(user=user,is_customer=True)
        except:
            pass
    return render(request,'customer/sign-up.html',context)