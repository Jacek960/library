from django.contrib import admin

# Register your models here.
from catalog.models import Book, Autor, Category, BookInstance

admin.site.register(Book)
admin.site.register(Autor)
admin.site.register(Category)
admin.site.register(BookInstance)


