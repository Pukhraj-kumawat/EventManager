from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate


def loginPage(request):
    user = 'Outside'
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            if request.user.is_authenticated:
                return HttpResponse("Already authenticated ")

            user = authenticate(request,username = username, password = password)

            if user is not None:
                return HttpResponse("authenticated ")
            else:
                return HttpResponse("Not authenticated ")
        except:
            pass
    context = {'user':user}    
    return render(request,'login.html',context)
