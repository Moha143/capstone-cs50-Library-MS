
from datetime import datetime
from django.contrib.auth import login, authenticate,  logout
from django.shortcuts import render, redirect
from Library import models
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models.deletion import RestrictedError
from datetime import datetime


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
    if user:
        return render(request, 'Member Panel/member_dash.html')
    else:
        return render(request, 'Library Panel/dash.html')


@login_required(login_url='Login')
def add_member(request):
    if request.user.is_staff == True:
        return render(request, 'Library Panel/Account/add-member.html')
    else:
        return render(request, 'base/notfound.html')


@login_required(login_url='Login')
def Profile(request):
    return render(request, 'Base/Profile.html')


@login_required(login_url='Login')
def member_list(request):
    if request.user.is_staff == True:
        return render(request, 'Library Panel/Account/member-list.html')
    else:
        return render(request, 'Library Panel/notfound.html')


@login_required(login_url='Login')
def staff_list(request):
    if request.user.is_staff == True:
        return render(request, 'Library Panel/Account/staff-list.html')
    else:
        return render(request, 'Library Panel/notfound.html')


@login_required(login_url='Login')
def add_staff(request):
    if request.user.is_staff == True:
        return render(request, 'Library Panel/Account/add-staff.html')
    else:
        return render(request, 'Base/notfound.html')


@login_required(login_url='Login')
def Author(request):
    if request.user.is_staff == True:
        return render(request, 'Library Panel/Library/Author.html')
    else:
        return render(request, 'Base/notfound.html')


@login_required(login_url='Login')
def Category(request):
    if request.user.is_staff == True:
        return render(request, 'Library Panel/Library/Category.html')
    else:
        return render(request, 'Base/notfound.html')


@login_required(login_url='Login')
def Book(request):
    if request.user.is_staff == True:
        return render(request, 'Library Panel/Library/Book.html')
    else:
        return render(request, 'Base/notfound.html')


@login_required(login_url='Login')
def Borrow(request):
    if request.user.is_staff == True:
        return render(request, 'Library Panel/Library/Borrow.html')
    else:
        return render(request, 'Base/notfound.html')


@login_required(login_url='Login')
def Reading(request):
    if request.user.is_staff == True:
        return render(request, 'Library Panel/Library/Reading.html')
    else:
        return render(request, 'Base/notfound.html')


@login_required(login_url='Login')
def MyReading(request):
    if request.user.is_member == True:
        return render(request, 'Member Panel/MyReading.html')
    else:
        return render(request, 'Base/notfound.html')


@login_required(login_url='Login')
def Fine(request):
    if request.user.is_staff == True:
        return render(request, 'Library Panel/Library/Fine.html')
    else:
        return render(request, 'Base/notfound.html')


@login_required(login_url='Login')
def Print_Book_Borrow(request):
    if request.user.is_staff == True:
        return render(request, 'Library Panel/Library/print_book_borrow.html')
    else:
        return render(request, 'Base/notfound.html')


@login_required(login_url='Login')
def print_fine(request):
    if request.user.is_staff == True:
        return render(request, 'Library Panel/Library/print_fine.html')
    else:
        return render(request, 'Base/notfound.html')


@login_required(login_url='Login')
def BookDetail(request, id):
    if request.user.is_staff == True:
        return render(request, 'Library Panel/Library/BookDetail.html', {'BookID': id})
    else:
        return render(request, 'Base/notfound.html')


@login_required(login_url='Login')
def add_staff(request):

    if request.user.is_staff == True:
        return render(request, 'Library Panel/Account/add-staff.html')
    else:
        return render(request, 'Base/notfound.html')


@login_required(login_url='Login')
def Add_payment(request):
    if request.user.is_staff == True:
        return render(request, 'Library Panel/Library/Add-payment.html')
    else:
        return render(request, 'Base/notfound.html')
# Data Management
# View Actions


@login_required(login_url='Login')
def ManageMember(request, id):
    if request.user.is_staff == True:
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
                if type == "getmember":
                    try:
                        Members = models.Account.objects.filter(
                            is_member=True)
                        message = []
                        for i in range(0, len(Members)):
                            message.append({
                                'id': Members[i].id,
                                'name': Members[i].first_name + ' ' + Members[i].last_name,

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
    else:
        return render(request, 'Base/notfound.html')


@login_required(login_url='Login')
def ManageStaff(request, id):
    if request.user.is_staff == True:
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
    else:
        return render(request, 'base/notfound.html')


@login_required(login_url='Login')
def ManageAuthor(request, id):
    if request.user.is_staff == True:
        type = request.POST.get('type')
        if id == 0:
            # Get All Auther
            if request.method == 'GET':

                Author = models.Author.objects.all()
                message = []
                for i in range(0, len(Author)):
                    message.append({
                        'id': Author[i].id,
                        'name': Author[i].name,
                        'created_at': Author[i].created_at,

                    })
                return JsonResponse({'isError': False, 'Message': message}, status=200)

            # Post new Author
            if request.method == 'POST':
                if type == "add":

                    FullName = request.POST.get('FName')

                    if models.Author.objects.filter(name=FullName).exists():
                        return JsonResponse({'isError': True, 'Message': 'Author Name already exists'})

                    else:
                        Author = models.Author(name=FullName)
                        Author.save()

                        message = {
                            'isError': False,
                            'Message': 'New Author has been successfuly registered'
                        }

                        return JsonResponse(message, status=200)
                if type == "get":
                    try:
                        Author = models.Author.objects.all()
                        message = []
                        for i in range(0, len(Author)):
                            message.append({
                                'id': Author[i].id,
                                'name': Author[i].name,
                                'created_at': Author[i].created_at,

                            })
                        return JsonResponse({'isError': False, 'Message': message}, status=200)

                    except Exception as error:
                        return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)

        else:

            if request.method == 'GET':
                try:
                    Author = models.Author.objects.get(id=id)

                    message = {
                        'id': Author.id,
                        'name': Author.name,

                    }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)

                except Exception as error:
                    return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)

            # Delete Member
            if request.method == 'DELETE':

                try:
                    AuthorDelete = models.Author.objects.get(id=id)
                    AuthorDelete.delete()
                    message = {
                        'isError': False,
                        'Message': 'Author has been successfully deleted'
                    }
                    return JsonResponse(message, status=200)
                except RestrictedError:
                    return JsonResponse({'isError': True, 'Message': 'Cannot delete, becouse it is restricted'}, status=200)

            # Update Staff
            if request.method == 'POST':
                FullName = request.POST.get('FName')

                try:
                    getAuthor = models.Author.objects.get(id=id)
                    if models.Author.objects.filter(name=FullName).exists() and getAuthor.name != FullName:
                        return JsonResponse({'isError': True, 'Message': 'Name already exists'})

                    else:
                        getAuthor.name = FullName

                        getAuthor.save()
                        return JsonResponse({'isError': False, 'Message': 'Author has been successfully updated'}, status=200)
                except Exception as error:

                    return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)
    else:
        return render(request, 'base/notfound.html')


@login_required(login_url='Login')
def ManageCategory(request, id):
    if request.user.is_staff == True:
        type = request.POST.get('type')
        if id == 0:
            # Get All Category
            if request.method == 'GET':

                Category = models.Category.objects.all()
                message = []
                for i in range(0, len(Category)):
                    message.append({
                        'id': Category[i].id,
                        'name': Category[i].name,
                        'created_at': Category[i].created_at,

                    })
                return JsonResponse({'isError': False, 'Message': message}, status=200)

            # Post new Category
            if request.method == 'POST':
                if type == "add":

                    CName = request.POST.get('CName')

                    if models.Category.objects.filter(name=CName).exists():
                        return JsonResponse({'isError': True, 'Message': 'Category Name already exists'})

                    else:
                        Category = models.Category(name=CName)
                        Category.save()

                        message = {
                            'isError': False,
                            'Message': 'New Category has been successfuly registered'
                        }

                        return JsonResponse(message, status=200)
                if type == "get":
                    try:
                        Category = models.Category.objects.all()
                        message = []
                        for i in range(0, len(Category)):
                            message.append({
                                'id': Category[i].id,
                                'name': Category[i].name,
                                'created_at': Category[i].created_at,

                            })
                        return JsonResponse({'isError': False, 'Message': message}, status=200)

                    except Exception as error:
                        return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)

        else:

            if request.method == 'GET':
                try:
                    Category = models.Category.objects.get(id=id)

                    message = {
                        'id': Category.id,
                        'name': Category.name,

                    }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)

                except Exception as error:
                    return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)

            # Delete Category
            if request.method == 'DELETE':

                try:
                    DeleteCategory = models.Category.objects.get(id=id)
                    DeleteCategory.delete()
                    message = {
                        'isError': False,
                        'Message': 'Category has been successfully deleted'
                    }
                    return JsonResponse(message, status=200)
                except RestrictedError:
                    return JsonResponse({'isError': True, 'Message': 'Cannot delete, becouse it is restricted'}, status=200)

            # Update Category
            if request.method == 'POST':
                CName = request.POST.get('CName')

                try:
                    GetCategory = models.Category.objects.get(id=id)
                    if models.Category.objects.filter(name=CName).exists() and GetCategory.name != CName:
                        return JsonResponse({'isError': True, 'Message': 'Name already exists'})

                    else:
                        GetCategory.name = CName
                        GetCategory.save()
                        return JsonResponse({'isError': False, 'Message': 'Category has been successfully updated'}, status=200)
                except Exception as error:

                    return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)

    else:
        return render(request, 'base/notfound.html')


@login_required(login_url='Login')
def ManageBook(request, id):
    if request.user.is_staff == True:
        type = request.POST.get('type')
        if id == "0":

            # Post new Book
            if request.method == 'POST':
                if type == "add":

                    Title = request.POST.get('Title')
                    Author = request.POST.get('Author')
                    Category = request.POST.get('Category')
                    ISBNs = request.POST.get('ISBN')
                    Coppy = request.POST.get('Coppy')
                    Available = request.POST.get('Available')
                    Publisher = request.POST.get('Publisher')
                    Summary = request.POST.get('Summary')

                    Avatar = request.FILES['Avatar']
                    try:
                        Author = models.Author.objects.get(id=Author)
                        Category = models.Category.objects.get(id=Category)

                        if models.Book.objects.filter(title=Title, author=Author, category=Category, ISBN=ISBNs).exists():
                            return JsonResponse({'isError': True, 'Message': 'This Book already exists'})
                        else:
                            Books = models.Book(title=Title, author=Author, category=Category, ISBN=ISBNs,
                                                copy=Coppy, available=Available, publisher=Publisher, summary=Summary, image=Avatar)
                            Books.save()

                            message = {
                                'isError': False,
                                'Message': 'New Books has been added successfuly'
                            }

                            return JsonResponse(message, status=200)
                    except Exception as error:
                        return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)
                if type == "get":
                    try:
                        Book = models.Book.objects.all()
                        message = []
                        for i in range(0, len(Book)):
                            message.append({
                                'id': Book[i].id,
                                'title': Book[i].title,
                                'author': Book[i].author.name,
                                'category': Book[i].category.name,
                                'copy': Book[i].copy,
                                'available': Book[i].available,
                                'created_at': Book[i].created_at,

                            })
                        return JsonResponse({'isError': False, 'Message': message}, status=200)

                    except Exception as error:
                        return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)

        else:

            if request.method == 'GET':
                try:
                    Book = models.Book.objects.get(id=id)

                    message = {
                        'id': Book.id,
                        'title': Book.title,
                        'summary': Book.summary,
                        'available': Book.available,
                        'ISBN': Book.ISBN,
                        'copy': Book.copy,
                        'summary': Book.summary,
                        'publisher': Book.publisher,
                        'authorid': Book.author.id,
                        'authorname': Book.author.name,
                        'categoryid': Book.category.id,
                        'categoryname': Book.category.name,
                        'categoryname': Book.category.name,
                        'image': str(Book.image),
                    }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)

                except Exception as error:
                    return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)

            # Delete Book
            if request.method == 'DELETE':

                try:
                    DeleteBook = models.Book.objects.get(id=id)
                    DeleteBook.delete()
                    message = {
                        'isError': False,
                        'Message': 'Book has been successfully deleted'
                    }
                    return JsonResponse(message, status=200)
                except RestrictedError:
                    return JsonResponse({'isError': True, 'Message': 'Cannot delete, becouse it is restricted'}, status=200)

            # Update Category
            if request.method == 'POST':
                Title = request.POST.get('Title')
                author = request.POST.get('Author')
                category = request.POST.get('Category')
                ISBNs = request.POST.get('ISBN')
                Coppy = request.POST.get('Coppy')
                Available = request.POST.get('Available')
                Publisher = request.POST.get('Publisher')
                Summary = request.POST.get('Summary')

                try:

                    Author = models.Author.objects.get(id=author)
                    Category = models.Category.objects.get(id=category)
                    GetBook = models.Book.objects.get(id=id)
                    if models.Book.objects.filter(title=Title, author=Author, category=Category, ISBN=ISBNs).exists() and GetBook.title != Title and GetBook.author != Author and GetBook.category != Category and GetBook.ISBN != ISBNs:
                        return JsonResponse({'isError': True, 'Message': 'This Book  already exists'})

                    else:
                        GetBook.title = Title
                        GetBook.author = Author
                        GetBook.category = Category
                        GetBook.ISBN = ISBNs
                        GetBook.copy = Coppy
                        GetBook.available = Available
                        GetBook.publisher = Publisher
                        GetBook.summary = Summary
                        GetBook.save()
                        return JsonResponse({'isError': False, 'Message': 'Book has been successfully updated'}, status=200)
                except Exception as error:

                    return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)
    else:
        return render(request, 'base/notfound.html')


@login_required(login_url='Login')
def ManageBookBorrow(request, id):
    if request.user.is_staff == True:
        type = request.POST.get('type')
        if id == 0:

            # Post new Book
            if request.method == 'POST':
                if type == "add":
                    Book = request.POST.get('Book')
                    Start = request.POST.get('Start')
                    End = request.POST.get('End')
                    Member = request.POST.get('Member')
                    NBook = int(request.POST.get('NBook'))

                    try:
                        MemberID = models.Account.objects.get(id=Member)
                        Bookss = models.Book.objects.get(id=Book)

                        if NBook <= int(Bookss.available):
                            Available = int(Bookss.available)-NBook
                            Book = models.Borrow(
                                status="Borrow", Member=MemberID, Book=Bookss, start_date=Start, end_date=End, NBook=NBook)

                            Bookss.available = Available
                            Book.save()
                            Bookss.save()

                            message = {
                                'isError': False,
                                'Message': 'New Books has been added successfuly'
                            }

                            return JsonResponse(message, status=200)

                        else:
                            return JsonResponse({'Message': ". This number is not available", 'isError': True, }, status=200)
                    except Exception as error:
                        return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)
                if type == "get":
                    try:
                        Borrow = models.Borrow.objects.all()
                        message = []
                        for i in range(0, len(Borrow)):
                            message.append({
                                'id': Borrow[i].id,
                                'BookName': Borrow[i].Book.title,
                                'NBook': Borrow[i].NBook,
                                'Status': Borrow[i].status,
                                'member': Borrow[i].Member.first_name + ' ' + Borrow[i].Member.first_name,
                                'author': Borrow[i].Book.author.name,
                                'BookID': Borrow[i].Book.id,
                                'category': Borrow[i].Book.category.name,
                                'start': PreviewDate(str(Borrow[i].start_date), False),
                                'end': PreviewDate(str(Borrow[i].end_date), False),
                                'created_at': PreviewDate(Borrow[i].created_at, True),
                            })
                        return JsonResponse({'isError': False, 'Message': message}, status=200)

                    except Exception as error:
                        return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)

        else:

            if request.method == 'GET':
                try:
                    BookBorrow = models.Borrow.objects.get(id=id)

                    message = {
                        'id': BookBorrow.id,
                        'status': BookBorrow.status,
                        'NBook': BookBorrow.NBook,
                        'start_date': BookBorrow.start_date,
                        'end_date': BookBorrow.end_date,
                        'BookID': BookBorrow.Book.id,
                        'BookName': BookBorrow.Book.title,
                        'Member': BookBorrow.Member.id,
                        'is_fine': BookBorrow.is_fine,
                        'Status': BookBorrow.status,
                        'member': BookBorrow.Member.first_name + ' ' + BookBorrow.Member.first_name,
                        'Phone': BookBorrow.Member.phone,
                        'author': BookBorrow.Book.author.name,
                        'category': BookBorrow.Book.category.name,
                        'start': PreviewDate(str(BookBorrow.start_date), False),
                        'end': PreviewDate(str(BookBorrow.end_date), False),
                    }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)

                except Exception as error:
                    return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)

            # Delete Book Borrow
            if request.method == 'DELETE':

                try:
                    DeleteBorrow = models.Borrow.objects.get(id=id)
                    DeleteBorrow.delete()
                    message = {
                        'isError': False,
                        'Message': 'Book Borrow has been successfully deleted'
                    }
                    return JsonResponse(message, status=200)
                except RestrictedError:
                    return JsonResponse({'isError': True, 'Message': 'Cannot delete, becouse it is restricted'}, status=200)

            # Update Book Borrow
            if request.method == 'POST':

                Book = request.POST.get('Book')
                Start = request.POST.get('Start')
                End = request.POST.get('End')
                Member = request.POST.get('Member')
                NBook = int(request.POST.get('NBook'))
                try:
                    MemberID = models.Account.objects.get(id=Member)
                    Bookss = models.Book.objects.get(id=Book)
                    gitBookBorrow = models.Borrow.objects.get(id=id)
                    if NBook <= int(Bookss.available):
                        gitBookBorrow.Member = MemberID
                        gitBookBorrow.Book = Bookss
                        gitBookBorrow.start_date = Start
                        gitBookBorrow.end_date = End
                        if NBook == int(gitBookBorrow.NBook):
                            available = int(Bookss.available)
                            av = available
                        elif NBook > int(gitBookBorrow.NBook):
                            available = NBook - int(gitBookBorrow.NBook)
                            av = int(Bookss.available)-available

                        else:
                            available = int(gitBookBorrow.NBook) - NBook
                            av = available+int(Bookss.available)

                        Bookss.available = av
                        gitBookBorrow.NBook = NBook
                        Bookss.save()
                        gitBookBorrow.save()

                        message = {
                            'isError': False,
                            'Message': ' Book Borrow has been updated successfuly'
                        }

                        return JsonResponse(message, status=200)

                    else:
                        return JsonResponse({'Message': ". This number is not available", 'isError': True, }, status=200)
                except Exception as error:
                    return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)
    else:
        return render(request, 'base/notfound.html')


@login_required(login_url='Login')
def ManageReading(request, id):
    if request.user.is_staff == True:
        type = request.POST.get('type')
        if id == 0:

            # Post new Book
            if request.method == 'POST':
                if type == "add":

                    time_in = request.POST.get('time_in')
                    time_out = request.POST.get('time_out')
                    Member = request.POST.get('Member')

                    try:
                        MemberID = models.Account.objects.get(id=Member)

                        Reading = models.Reading(
                            Member=MemberID, time_in=time_in, time_out=time_out)

                        Reading.save()
                        message = {
                            'isError': False,
                            'Message': MemberID.first_name+" "+MemberID.last_name + ' has been added successfuly reading books'
                        }

                        return JsonResponse(message, status=200)

                    except Exception as error:
                        return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)
                if type == "get":
                    try:
                        Reading = models.Reading.objects.all()
                        message = []
                        for i in range(0, len(Reading)):
                            time_outs = str(Reading[i].time_out).split(
                                ':')[0] + ':' + str(Reading[i].time_out).split(':')[1]
                            time_ins = str(Reading[i].time_in).split(
                                ':')[0] + ':' + str(Reading[i].time_in).split(':')[1]
                            message.append({
                                'id': Reading[i].id,
                                'member': Reading[i].Member.first_name + ' ' + Reading[i].Member.first_name,
                                'time_out': shorttime(time_outs),
                                'time_in': shorttime(time_ins),
                                'Phone': Reading[i].Member.phone,
                                'created_at': PreviewDate(Reading[i].created_at, True),
                            })
                        return JsonResponse({'isError': False, 'Message': message}, status=200)

                    except Exception as error:
                        return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)

        else:

            if request.method == 'GET':
                try:
                    Reading = models.Reading.objects.get(id=id)

                    message = {
                        'id': Reading.id,
                        'memberName': Reading.Member.first_name + ' ' + Reading.Member.first_name,
                        'member': Reading.Member.id,
                        'time_in': Reading.time_in,
                        'time_out': Reading.time_out,
                        'Phone': Reading.Member.phone,
                        'created_at': PreviewDate(Reading.created_at, True),
                    }
                    return JsonResponse({'isError': False, 'Message': message}, status=200)

                except Exception as error:
                    return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)

            # Delete Book Reading
            if request.method == 'DELETE':

                try:
                    DeleteReading = models.Reading.objects.get(id=id)
                    DeleteReading.delete()
                    message = {
                        'isError': False,
                        'Message': 'Member Reading has been successfully deleted'
                    }
                    return JsonResponse(message, status=200)
                except RestrictedError:
                    return JsonResponse({'isError': True, 'Message': 'Cannot delete, becouse it is restricted'}, status=200)

            # Update Book Reading
            if request.method == 'POST':

                time_in = request.POST.get('time_in')
                time_out = request.POST.get('time_out')
                Member = request.POST.get('Member')
                try:
                    MemberID = models.Account.objects.get(id=Member)
                    Reading = models.Reading.objects.get(id=id)
                    Reading.Member = MemberID
                    Reading.time_in = time_in
                    Reading.time_out = time_out
                    Reading.save()

                    message = {
                        'isError': False,
                        'Message': MemberID.first_name+" "+MemberID.last_name + ' has been updated successfuly reading books'
                    }

                    return JsonResponse(message, status=200)

                except Exception as error:
                    return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)

    else:
        return render(request, 'base/notfound.html')


@login_required(login_url='Login')
def ManageFine(request, id):
    if request.user.is_staff == True:
        type = request.POST.get('type')
        if id == 0:
            if type == "get":
                try:
                    Fine = models.Fine.objects.all()
                    message = []
                    for i in range(0, len(Fine)):
                        message.append({
                            'id': Fine[i].id,
                            'member': Fine[i].borrow.Member.first_name + ' ' + Fine[i].borrow.Member.first_name,
                            'phone': Fine[i].borrow.Member.phone,
                            'book': Fine[i].borrow.Book.title,
                            'amount': "$ " + Fine[i].amount,
                            'paid': "$ "+Fine[i].paid,

                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)

                except Exception as error:
                    return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)
            if type == "memberbook":
                Member = request.POST.get('Member')
                try:
                    MemberBook = models.Borrow.objects.filter(
                        Member=Member, status="Not Returned")
                    message = []
                    for i in range(0, len(MemberBook)):
                        message.append({
                            'id': MemberBook[i].id,
                            'book': MemberBook[i].Book.title,
                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)

                except Exception as error:
                    return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)
            if type == "finedetails":
                Member = request.POST.get('Member')
                borrow = request.POST.get('borrow')
                try:
                    Borrowdetail = models.Fine.objects.filter(
                        borrow=borrow)
                    message = []
                    for i in range(0, len(Borrowdetail)):
                        message.append({
                            'id': Borrowdetail[i].id,
                            'start': PreviewDate(str(Borrowdetail[i].borrow.start_date), False),
                            'end':  PreviewDate(str(Borrowdetail[i].borrow.end_date), False),
                            'amount': Borrowdetail[i].amount,
                            'paid': Borrowdetail[i].paid,
                            'remaining': float(Borrowdetail[i].amount) - float(Borrowdetail[i].paid),
                        })
                    return JsonResponse({'isError': False, 'Message': message}, status=200)

                except Exception as error:
                    return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)

        else:

            # Delete Fine
            if request.method == 'DELETE':

                try:
                    deletefine = models.Fine.objects.get(id=id)
                    deletefine.delete()
                    message = {
                        'isError': False,
                        'Message': 'Fine  has been successfully deleted'
                    }
                    return JsonResponse(message, status=200)
                except RestrictedError:
                    return JsonResponse({'isError': True, 'Message': 'Cannot delete, becouse it is restricted'}, status=200)

            # Adding Fine payment m
            if request.method == 'POST':
                paid = float(request.POST.get('fines'))
                borrowID = request.POST.get('borrow')
                Member = request.POST.get('Member')
                try:
                    Borrows = models.Borrow.objects.get(id=borrowID)
                    Fine = models.Fine.objects.get(id=id)
                    remaining = float(Fine.amount) - float(Fine.paid)
                    if remaining == 0:
                        return JsonResponse({'Message': ". Payment already paid", 'isError': True, }, status=200)
                    else:
                        total = float(Fine.paid)+paid
                        if total == float(Fine.amount):
                            Borrows.status = "Returned"
                            Books = models.Book.objects.get(id=Borrows.Book.id)
                            av = int(Books.available)+int(Borrows.NBook)
                            Books.available = av
                            Books.save()
                            Borrows.save()
                        Fine.paid = total
                        Fine.borrow = Borrows
                        Fine.save()
                        message = {
                            'isError': False,
                            'Message': Borrows.Member.first_name+" "+Borrows.Member.last_name + ' has paid fine'
                        }

                        return JsonResponse(message, status=200)

                except Exception as error:
                    return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)

    else:
        return render(request, 'base/notfound.html')


@login_required(login_url='Login')
def ManageDashboard(request, id):
    if request.user.is_staff == True:
        type = request.POST.get('type')
        if id == 0:

            # Post new Book
            if request.method == 'POST':

                if type == "getbook":
                    Author = request.POST.get('Author')
                    Category = request.POST.get('Category')
                    try:
                        BookArgs = {}

                        if Author != 'All':
                            BookArgs['author'] = Author
                        if Category != 'All':
                            BookArgs['category'] = Category
                        Book = models.Book.objects.filter(**BookArgs)
                        message = []
                        for i in range(0, len(Book)):
                            message.append({
                                'id': Book[i].id,
                                'title': Book[i].title,
                                'image': str(Book[i].image),

                            })
                        return JsonResponse({'isError': False, 'Message': message}, status=200)

                    except Exception as error:
                        return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)

                if type == "getusers":
                    try:
                        member = models.Account.objects.filter(
                            is_member=True).count()
                        Staff = models.Account.objects.filter(
                            is_staff=True).count()
                        books = models.Book.objects.all().count()
                        message = []
                        message.append({
                            'members': member,
                            'staff': Staff,
                            'books': books,
                            'total': int(Staff)+int(member),


                        })
                        return JsonResponse({'isError': False, 'Message': message}, status=200)

                    except Exception as error:
                        return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)
    else:
        return render(request, 'base/notfound.html')


@login_required(login_url='Login')
def MemberDashbord(request, id):
    if request.user.is_member == True:
        type = request.POST.get('type')
        if id == 0:

            # Post new Book
            if request.method == 'POST':

                if type == "getbook":
                    Author = request.POST.get('Author')
                    Category = request.POST.get('Category')
                    Member = request.POST.get('Member')
                    try:
                        BookArgs = {}

                        if Author != 'All':
                            BookArgs['author'] = Author
                        if Category != 'All':
                            BookArgs['category'] = Category
                        Book = models.Borrow.objects.filter(Member=Member)
                        message = []
                        for i in range(0, len(Book)):
                            message.append({
                                'id': Book[i].Book.id,
                                'title': Book[i].Book.title,
                                'image': str(Book[i].Book.image),

                            })
                        return JsonResponse({'isError': False, 'Message': message}, status=200)

                    except Exception as error:
                        return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)

                if type == "getdashboard":
                    Member = request.POST.get('Member')
                    try:

                        books = models.Borrow.objects.filter(
                            Member=Member).count()
                        message = []
                        message.append({
                            'books': books,

                        })
                        return JsonResponse({'isError': False, 'Message': message}, status=200)

                    except Exception as error:
                        return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)

                if type == "getAuthor":
                    try:
                        Author = models.Author.objects.all()
                        message = []
                        for i in range(0, len(Author)):
                            message.append({
                                'id': Author[i].id,
                                'name': Author[i].name,

                            })
                        return JsonResponse({'isError': False, 'Message': message}, status=200)

                    except Exception as error:
                        return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)

                if type == "getCategory":
                    try:
                        Category = models.Category.objects.all()
                        message = []
                        for i in range(0, len(Category)):
                            message.append({
                                'id': Category[i].id,
                                'name': Category[i].name,

                            })
                        return JsonResponse({'isError': False, 'Message': message}, status=200)

                    except Exception as error:
                        return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)

                if type == "getmyreading":
                    Member = request.POST.get('Member')
                    try:
                        Reading = models.Reading.objects.filter(Member=Member)
                        message = []
                        for i in range(0, len(Reading)):
                            time_outs = str(Reading[i].time_out).split(
                                ':')[0] + ':' + str(Reading[i].time_out).split(':')[1]
                            time_ins = str(Reading[i].time_in).split(
                                ':')[0] + ':' + str(Reading[i].time_in).split(':')[1]
                            message.append({

                                'time_out': shorttime(time_outs),
                                'time_in': shorttime(time_ins),
                                'created_at': PreviewDate(Reading[i].created_at, True),
                            })
                        return JsonResponse({'isError': False, 'Message': message}, status=200)

                    except Exception as error:
                        return JsonResponse({'Message': str(error)+". Please contact ICT office", 'isError': True, }, status=200)

    else:
        return render(request, 'base/notfound.html')


def PreviewDate(date_string, is_datetime):
    if is_datetime:
        new_date = date_string
        date_string = new_date.strftime("%a") + ', ' + new_date.strftime(
            "%b") + ' ' + str(new_date.day) + ', ' + str(new_date.year) + '  ' + new_date.strftime("%I") + ':' + new_date.strftime("%M") + ':' + new_date.strftime("%S") + ' ' + new_date.strftime("%p")
    else:
        date_string = str(date_string)
        date_string = date_string.split('-')

        new_date = datetime(int(date_string[0]), int(
            date_string[1]), int(date_string[2]))

        date_string = new_date.strftime("%a") + ', ' + new_date.strftime(
            "%b") + ' ' + str(new_date.day) + ', ' + str(new_date.year)

    return date_string


def shorttime(time):
    # s = datetime.strptime(str(time), "%H:%M")
    s = datetime.strptime(time, "%H:%M")
    return s.strftime("%r")
