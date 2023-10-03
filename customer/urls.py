from django.urls import path
from . import views



urlpatterns = [
    path('book/<int:pk>/',views.book),    
    path('home-C/',views.home),
    path('full-package/<int:pk>/',views.full_package),
    path('booked/<int:venue_id>/',views.create_book),
    path('create-book/',views.create_book),
    path('delete-book/',views.delete_book),
    path('booked/',views.booked),
    path('save-date-time/<int:pk>/',views.save_date_time),
]