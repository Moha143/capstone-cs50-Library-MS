from django.contrib.auth import login, authenticate,  logout
from django.shortcuts import render, redirect
from . import models
# Create your views here.
from django.contrib.auth.decorators import login_required


def Login(request):

    if request.user.is_authenticated == False:

        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('Dashboard')
            else:
                return render(request, 'Library Panel/Account/login.html', {
                    "message": "Invalid username and/or password."
                })

        return render(request, 'Library Panel/Account/login.html')
    else:
        return redirect('Dashboard')


@login_required(login_url='Login')
def Main(request):
    user = request.user.is_member
    # Getch the two letters from the username
    if user:
        return render(request, 'Library Panel/dash.html')
    else:
        return render(request, 'Member Panel/member_dash.html')
