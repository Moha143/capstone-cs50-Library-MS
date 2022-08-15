from django.contrib.auth import login, authenticate,  logout
from django.shortcuts import render, redirect
from . import models
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models.deletion import RestrictedError


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
        return render(request, 'Member Panel/member_dash.html')
    else:
        return render(request, 'Library Panel/dash.html')


@login_required(login_url='Login')
def add_member(request):
    return render(request, 'Library Panel/Account/add-member.html')


@login_required(login_url='Login')
def member_list(request):
    return render(request, 'Library Panel/Account/member-list.html')


@login_required(login_url='Login')
def staff_list(request):
    return render(request, 'Library Panel/Account/staff-list.html')


@login_required(login_url='Login')
def add_staff(request):
    return render(request, 'Library Panel/Account/add-staff.html')

# Data Management
# View Actions


@login_required(login_url='Login')
def ManageMember(request, id):
    type = request.POST.get('type')
    if id == 0:
        # Get All Staff
        if request.method == 'GET':

            Members = models.Account.objects.filter(
                is_member=True)
            message = []
            for i in range(0, len(Members)):
                message.append({
                    'id': Members[i].id,
                    'first_name': Members[i].first_name,
                    'last_name': Members[i].last_name,
                    'name': Members[i].first_name + ' ' + Members[i].last_name,
                    'email': Members[i].email,
                    'phone': Members[i].phone,
                    'username': Members[i].username,
                    'date_joined': Members[i].date_joined,
                    'avatar': str(Members[i].avatar),
                    'is_active': Members[i].is_active,
                })
            return JsonResponse({'isError': False, 'Message': message}, status=200)

        # Post new Member
        if request.method == 'POST':
            if type == "add":

                FirstName = request.POST.get('FName')
                LastName = request.POST.get('LName')
                Email = request.POST.get('Email')
                Phone = request.POST.get('Phone')
                Gender = request.POST.get('Gender')
                Username = request.POST.get('Username')
                Avatar = request.FILES['Avatar']
                if models.Account.objects.filter(email=Email).exists():
                    return JsonResponse({'isError': True, 'Message': 'Email already exists'})
                elif models.Account.objects.filter(username=Username).exists():
                    return JsonResponse({'isError': True, 'Message': 'Username already exists'})

                else:
                    Member = models.Account.objects.create_user(username=Username,
                                                                email=Email, first_name=FirstName, last_name=LastName, phone=Phone, gender=Gender, is_member=True, avatar=Avatar, password="123")
                    Member.save()

                    message = {
                        'isError': False,
                        'Message': 'New Member has been successfuly registered'
                    }

                    return JsonResponse(message, status=200)
            if type == "get":
                try:
                    Members = models.Account.objects.filter(
                        is_member=True)
                    message = []
                    for i in range(0, len(Members)):
                        message.append({
                            'id': Members[i].id,
                            'first_name': Members[i].first_name,
                            'last_name': Members[i].last_name,
                            'name': Members[i].first_name + ' ' + Members[i].last_name,
                            'email': Members[i].email,
                            'phone': Members[i].phone,
                            'gender': Members[i].gender,
                            'username': Members[i].username,
                            'date_joined': Members[i].date_joined,
                            'avatar': str(Members[i].avatar),
                            'is_active': Members[i].is_active,
                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                except Exception as error:
                    return JsonResponse({'Message': str(error)+" Something is wrong please contact ICT office", 'isError': True, }, status=200)

    else:

        if request.method == 'GET':
            try:
                Member = models.Account.objects.get(id=id)

                message = {
                    'id': Member.id,
                    'first_name': Member.first_name,
                    'last_name': Member.last_name,
                    'email': Member.email,
                    'phone': Member.phone,
                    'gender': Member.gender,
                    'username': Member.username,
                    'is_Member': Member.is_member,
                    'avatar': str(Member.avatar)
                }
                return JsonResponse({'isError': False, 'Message': message}, status=200)

            except Exception as error:
                return JsonResponse({'Message': str(error)+" Something is wrong please contact ICT office", 'isError': True, }, status=200)

        # Delete Member
        if request.method == 'DELETE':

            try:
                memberDelete = models.Account.objects.get(id=id)
                memberDelete.delete()
                message = {
                    'isError': False,
                    'Message': 'Member has been successfully deleted'
                }
                return JsonResponse(message, status=200)
            except RestrictedError:
                return JsonResponse({'isError': True, 'Message': 'Cannot delete, becouse it is restricted'}, status=200)

        # Update Member
        if request.method == 'POST':
            FirstName = request.POST.get('FName')
            LastName = request.POST.get('LName')
            Email = request.POST.get('Email')
            Phone = request.POST.get('Phone')
            Gender = request.POST.get('Gender')
            Username = request.POST.get('Username')
            try:
                GetMember = models.Account.objects.get(id=id)
                if models.Account.objects.filter(email=Email).exists() and GetMember.email != Email:
                    return JsonResponse({'isError': True, 'Message': 'Email already exists'})
                elif models.Account.objects.filter(username=Username).exists() and GetMember.username != Username:
                    return JsonResponse({'isError': True, 'Message': 'Username already exists'})
                else:
                    GetMember.first_name = FirstName
                    GetMember.last_name = LastName
                    GetMember.username = Username
                    GetMember.email = Email
                    GetMember.phone = Phone
                    GetMember.gender = Gender
                    GetMember.save()
                    return JsonResponse({'isError': False, 'Message': 'Member has been successfully updated'}, status=200)
            except Exception as error:

                return JsonResponse({'Message': str(error)+" Something is wrong please contact ICT office", 'isError': True, }, status=200)


@login_required(login_url='Login')
def ManageStaff(request, id):
    type = request.POST.get('type')
    if id == 0:
        # Get All Staff
        if request.method == 'GET':

            Staff = models.Account.objects.filter(
                is_member=True)
            message = []
            for i in range(0, len(Staff)):
                message.append({
                    'id': Staff[i].id,
                    'first_name': Staff[i].first_name,
                    'last_name': Staff[i].last_name,
                    'name': Staff[i].first_name + ' ' + Staff[i].last_name,
                    'email': Staff[i].email,
                    'phone': Staff[i].phone,
                    'username': Staff[i].username,
                    'date_joined': Staff[i].date_joined,
                    'avatar': str(Staff[i].avatar),
                    'is_active': Staff[i].is_active,
                })
            return JsonResponse({'isError': False, 'Message': message}, status=200)

        # Post new Staff
        if request.method == 'POST':
            if type == "add":

                FirstName = request.POST.get('FName')
                LastName = request.POST.get('LName')
                Email = request.POST.get('Email')
                Phone = request.POST.get('Phone')
                Gender = request.POST.get('Gender')
                Username = request.POST.get('Username')
                Avatar = request.FILES['Avatar']
                if models.Account.objects.filter(email=Email).exists():
                    return JsonResponse({'isError': True, 'Message': 'Email already exists'})
                elif models.Account.objects.filter(username=Username).exists():
                    return JsonResponse({'isError': True, 'Message': 'Username already exists'})

                else:
                    Staff = models.Account.objects.create_user(username=Username,
                                                               email=Email, first_name=FirstName, last_name=LastName, phone=Phone, gender=Gender, is_member=False, avatar=Avatar, password="123")
                    Staff.save()

                    message = {
                        'isError': False,
                        'Message': 'New Staff has been successfuly registered'
                    }

                    return JsonResponse(message, status=200)
            if type == "get":
                try:
                    Staff = models.Account.objects.filter(
                        is_member=False)
                    message = []
                    for i in range(0, len(Staff)):
                        message.append({
                            'id': Staff[i].id,
                            'first_name': Staff[i].first_name,
                            'last_name': Staff[i].last_name,
                            'name': Staff[i].first_name + ' ' + Staff[i].last_name,
                            'email': Staff[i].email,
                            'phone': Staff[i].phone,
                            'gender': Staff[i].gender,
                            'username': Staff[i].username,
                            'date_joined': Staff[i].date_joined,
                            'avatar': str(Staff[i].avatar),
                            'is_active': Staff[i].is_active,
                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)
                except Exception as error:
                    return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)

    else:

        if request.method == 'GET':
            try:
                Staff = models.Account.objects.get(id=id)

                message = {
                    'id': Staff.id,
                    'first_name': Staff.first_name,
                    'last_name': Staff.last_name,
                    'email': Staff.email,
                    'phone': Staff.phone,
                    'gender': Staff.gender,
                    'username': Staff.username,
                    'avatar': str(Staff.avatar)
                }
                return JsonResponse({'isError': False, 'Message': message}, status=200)

            except Exception as error:
                return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)

        # Delete Member
        if request.method == 'DELETE':

            try:
                StaffDelete = models.Account.objects.get(id=id)
                StaffDelete.delete()
                message = {
                    'isError': False,
                    'Message': 'Staff has been successfully deleted'
                }
                return JsonResponse(message, status=200)
            except RestrictedError:
                return JsonResponse({'isError': True, 'Message': 'Cannot delete, becouse it is restricted'}, status=200)

        # Update Staff
        if request.method == 'POST':
            FirstName = request.POST.get('FName')
            LastName = request.POST.get('LName')
            Email = request.POST.get('Email')
            Phone = request.POST.get('Phone')
            Gender = request.POST.get('Gender')
            Username = request.POST.get('Username')
            try:
                GetStaff = models.Account.objects.get(id=id)
                if models.Account.objects.filter(email=Email).exists() and GetStaff.email != Email:
                    return JsonResponse({'isError': True, 'Message': 'Email already exists'})
                elif models.Account.objects.filter(username=Username).exists() and GetStaff.username != Username:
                    return JsonResponse({'isError': True, 'Message': 'Username already exists'})
                else:
                    GetStaff.first_name = FirstName
                    GetStaff.last_name = LastName
                    GetStaff.username = Username
                    GetStaff.email = Email
                    GetStaff.phone = Phone
                    GetStaff.gender = Gender
                    GetStaff.save()
                    return JsonResponse({'isError': False, 'Message': 'Staff has been successfully updated'}, status=200)
            except Exception as error:

                return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)
