from django.contrib.auth import login, authenticate,  logout
from django.shortcuts import render, redirect
from . import models
# Create your views here.


def Login(request):
    # Checking if the user is logged in
    if request.user.is_authenticated == False:
        # Checking if the send request
        if request.method == 'POST':
            email = request.POST.get('Email').lower()
            password = request.POST.get('Password')
            # create instance from the user
            user = authenticate(email=email, password=password)

            # check if user created
            if user is not None:

                return redirect('Dashboard')

        return render(request, 'Library Panel/Account/login.html')
    else:
        return redirect('Dashboard')
