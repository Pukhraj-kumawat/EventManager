from django.urls import path
from . import views

urlpatterns = [
    path('',views.home),
    path('sign-up/',views.signUp),
]

