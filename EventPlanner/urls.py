from django.urls import path
from . import views

urlpatterns = [
    path('',views.home),
    path('sign-up-E/',views.signUp),
    path('login-E/',views.loginPage),
    path('logout/',views.logoutPage),
    path('logged-in-E/',views.loggedIn),
]

