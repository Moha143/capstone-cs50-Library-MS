# Generated by Django 4.1 on 2022-08-15 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Library', '0003_rename_subject_book_copy_remove_book_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='Author',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='Copy',
            new_name='copy',
        ),
    ]
