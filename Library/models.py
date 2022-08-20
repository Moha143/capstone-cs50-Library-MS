
import datetime
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Account(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, null=False,
                             blank=False)
    gender = models.CharField(max_length=50, null=True, blank=True)
    is_member = models.BooleanField(default=False)
    avatar = models.FileField(upload_to="avatars/",
                              default="avatars/avatar.jpg")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'account'


class Author(models.Model):
    name = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=datetime.datetime.today)

    class Meta:
        db_table = 'author'


class Category(models.Model):
    name = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=datetime.datetime.today)

    class Meta:
        db_table = 'category'


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=500, null=True)
    summary = models.CharField(max_length=500, null=True)
    author = models.ForeignKey(
        Author, on_delete=models.RESTRICT)
    ISBN = models.CharField(max_length=20)
    publisher = models.CharField(max_length=20)
    available = models.CharField(max_length=20)
    copy = models.CharField(max_length=20)

    category = models.ForeignKey(
        Category, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(default=datetime.datetime.today)
    image = models.FileField(upload_to="book/",
                             default="book/book.jpg")

    class Meta:
        db_table = 'book'


class Borrow(models.Model):
    status = models.CharField(max_length=20)
    NBook = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    Book = models.ForeignKey(
        Book, on_delete=models.RESTRICT)
    Member = models.ForeignKey(
        Account, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(default=datetime.datetime.today)
    is_fine = models.BooleanField(default=False)

    class Meta:
        db_table = 'borrow'


class Fine(models.Model):
    amount = models.CharField(max_length=100)
    paid = models.CharField(max_length=100)
    borrow = models.ForeignKey(
        Borrow, on_delete=models.RESTRICT)

    class Meta:
        db_table = 'fine'


class Reading(models.Model):
    time_in = models.TimeField()
    time_out = models.TimeField()
    Member = models.ForeignKey(
        Account, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(default=datetime.datetime.today)

    class Meta:
        db_table = 'reading'
