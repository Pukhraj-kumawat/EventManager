from django.urls import path
from . import views

urlpatterns = [
    path('',views.home),
    path('sign-up-<str:user_type>/',views.signUp),
    path('login-E/',views.loginPage),
    path('logout/',views.logoutPage),
    path('logged-in-E/',views.loggedIn),
    path('profile/<int:pk>/',views.profile),
    path('change-password/',views.ChangePassword),
    
]

