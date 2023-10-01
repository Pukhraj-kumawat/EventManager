from django.forms import ModelForm,FileInput
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import UserProfile,Venue,Event,Image


class SignUpForm(UserCreationForm):
    first_name =forms.CharField(max_length=30,required=True,
      validators=[
            RegexValidator(
                regex='^[A-Z,a-z, ]+$',
                message='First name must contain only alphabetic characters.',
                code='invalid_first_name'
            )
        ]
    )
    last_name =forms.CharField(max_length=30,required=True,
    validators=[
            RegexValidator(
                regex='^[A-Z,a-z, ]+$',
                message='First name must contain only alphabetic characters.',
                code='invalid_first_name'
            )
        ]
    )
    email = forms.EmailField(max_length=255, required=True)
    # To override custom validation error message -- >
            # username = forms.CharField(error_messages={'unique': 'Already taken choose another one'})

    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','password1','password2']

        
class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        widgets = {'profile_picture':FileInput()}
        fields = '__all__' 
        exclude = ('user_type','user',)
                      

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']


class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = '__all__'            
        exclude = ('vendors','category',)

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        exclude = ('event_planner',)

class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['image',]