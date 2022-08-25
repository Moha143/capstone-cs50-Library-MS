from django.urls import path
from . import views

urlpatterns = [
    # View
    path('dashboard', views.Main, name='Dashboard'),
    path('member_list', views.member_list, name='member_list'),
    path('add_member', views.add_member, name='add_member'),
    path('staff_list', views.staff_list, name='staff_list'),
    path('add_staff', views.add_staff, name='add_staff'),
    path('Author', views.Author, name='Author'),
    path('Category', views.Category, name='Category'),
    path('Book', views.Book, name='Book'),
    path('Borrow', views.Borrow, name='Borrow'),
    path('Reading', views.Reading, name='Reading'),
    path('MyReading', views.MyReading, name='MyReading'),
    path('MemberFineList', views.MemberFineList, name='MemberFineList'),
    path('Fine', views.Fine, name='Fine'),
    path('Print_Book_Borrow', views.Print_Book_Borrow, name='Print_Book_Borrow'),
    path('print_fine', views.print_fine, name='print_fine'),
    path('Profile', views.Profile, name='Profile'),
    path('Add_payment', views.Add_payment, name='Add_payment'),
    path('BookDetail/<str:id>', views.BookDetail, name='BookDetail'),



    # Data
    path('manage_member/<int:id>', views.ManageMember, name='manage_members'),
    path('manage_staff/<int:id>', views.ManageStaff, name='ManageStaff'),
    path('manage_author/<int:id>', views.ManageAuthor, name='ManageAuthor'),
    path('manage_category/<int:id>', views.ManageCategory, name='ManageCategory'),
    path('manage_book/<str:id>', views.ManageBook, name='ManageBook'),
    path('manage_bookborrow/<int:id>',
         views.ManageBookBorrow, name='ManageBookBorrow'),
    path('manage_fine/<int:id>', views.ManageFine, name='ManageFine'),
    path('manage_reading/<int:id>', views.ManageReading, name='ManageReading'),
    path('manage_dashboard/<int:id>', views.ManageDashboard, name='ManageReading'),
    path('manage_member_dashbord/<int:id>',
         views.MemberDashbord, name='MemberDashbord'),
]
