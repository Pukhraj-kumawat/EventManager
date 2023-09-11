from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.loginPage),
    path('',include('EventPlanner.urls')),
    path('',include('customer.urls')),
]
