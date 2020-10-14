from django import forms

from catalog.models import Book, Autor, BookInstance, Category


class BookForm(forms.ModelForm):
    class Meta:
        model=Book
        fields = ['title','category','description','autor','cover']


class AuthorForm(forms.ModelForm):
    class Meta:
        model=Autor
        fields = ['name',]

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields = ['name',]

class BookInstanceForm(forms.ModelForm):
    class Meta:
        model=BookInstance
        fields = ['book','imprint','borrower','status']





