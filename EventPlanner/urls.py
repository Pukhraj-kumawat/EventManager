from django.urls import path
from . import views

urlpatterns = [
    path('sign-up-<str:user_type>/',views.signUp),
    path('login-E/',views.loginPage),
    path('logout/',views.logoutPage),
    path('home-E/',views.home),
    path('profile/<int:pk>/',views.profile),
    path('edit-profile/<int:pk>/',views.edit_profile),
    path('change-password/',views.ChangePassword),
    path('event-planner-info/<int:pk>/',views.EventPlannerInfo),
    path('venue-info/<int:pk>/',views.VenueInfo),
    path('delete-account/',views.DeleteAccount),
    path('confirm-delete/',views.confirmDelete),
    path('create-message/',views.create_messages),
    path('create-event/',views.create_event),
    path('accept-booking/<int:pk>/<str:status>/',views.accept_booking),
]

