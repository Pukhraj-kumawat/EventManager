from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from EventPlanner.models import Venue


class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = '__all__'




