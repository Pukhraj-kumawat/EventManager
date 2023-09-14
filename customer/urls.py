from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:pk>/',views.book),
    path('login-C/',views.loginPage),
    path('logged-in-C/',views.loggedIn),
]
