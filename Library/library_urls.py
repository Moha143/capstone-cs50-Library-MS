from django.urls import path
from . import views

urlpatterns = [
    # View
    path('dashboard', views.Main, name='Dashboard'),
    path('member_list', views.member_list, name='member_list'),
    path('add_member', views.add_member, name='add_member'),
    path('staff_list', views.staff_list, name='staff_list'),
    path('add_staff', views.add_staff, name='add_staff'),



    # Data
    path('manage_member/<int:id>', views.ManageMember, name='manage_members'),
    path('manage_staff/<int:id>', views.ManageStaff, name='ManageStaff'),
]
