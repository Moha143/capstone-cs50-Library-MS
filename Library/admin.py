from django.contrib import admin

# Register your models here.
from django.contrib import admin
from Library import models as library_models

admin.site.register(library_models.Account)
admin.site.register(library_models.Author)
admin.site.register(library_models.Category)
admin.site.register(library_models.Borrow)
admin.site.register(library_models.Fine)
admin.site.register(library_models.Reading)
