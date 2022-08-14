from django.urls import path
from . import views

urlpatterns = [
    # View
    path('dashboard', views.Main, name='Dashboard'),
]
