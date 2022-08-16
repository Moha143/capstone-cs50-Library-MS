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


@login_required(login_url='Login')
def Author(request):
    return render(request, 'Library Panel/Library/Author.html')


@login_required(login_url='Login')
def Category(request):
    return render(request, 'Library Panel/Library/Category.html')


@login_required(login_url='Login')
def Book(request):
    return render(request, 'Library Panel/Library/Book.html')


@login_required(login_url='Login')
def BookDetail(request, id):
    return render(request, 'Library Panel/Library/BookDetail.html', {'BookID': id})


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


@login_required(login_url='Login')
def ManageAuthor(request, id):
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

        # Post new Staff
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


@login_required(login_url='Login')
def ManageCategory(request, id):
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


@login_required(login_url='Login')
def ManageBook(request, id):
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
@login_required(login_url='Login')
def ManageBookBorrow(request, id):
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
