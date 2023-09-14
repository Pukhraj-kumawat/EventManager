from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import UserProfile


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
    email = forms.EmailField(max_length=255, required=False)
    # To override custom validation error message -- >
            # username = forms.CharField(error_messages={'unique': 'Already taken choose another one'})

    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','password1','password2']

        
class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'       

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']


            
