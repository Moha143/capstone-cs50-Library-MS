# Generated by Django 4.1 on 2022-08-15 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Library', '0004_rename_author_book_author_rename_copy_book_copy'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='Category',
            new_name='category',
        ),
    ]
