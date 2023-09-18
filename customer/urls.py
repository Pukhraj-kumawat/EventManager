from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:pk>/',views.book),
    path('login-C/',views.loginPage),
    path('logged-in-C/',views.loggedIn),
    path('full-package/<int:pk>/',views.full_package),
    path('booked/<int:venue_id>/',views.create_book),
    path('create-book/',views.create_book),
    path('delete-book/',views.delete_book),
    path('booked/',views.booked),
]