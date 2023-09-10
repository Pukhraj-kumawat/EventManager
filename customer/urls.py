from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:pk>/',views.book),
    path('sign-up-C/',views.signUp),
]
