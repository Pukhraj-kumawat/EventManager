from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from EventPlanner.models import Venue
from .models import Messages


class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = '__all__'

class MessageForm(ModelForm):
    class Meta:
        model = Messages
        fields = ['message']
        widgets = {
            'message': forms.TextInput(attrs={'placeholder': 'Type..'}),
        }
        


