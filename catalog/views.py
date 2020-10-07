from django.shortcuts import render

# Create your views here.
from django.views import View

from catalog.models import Book, BookInstance, Autor


class HomePageView(View):
    def get(self,request):
        num_books = Book.objects.all().count()
        num_instances = BookInstance.objects.all().count()
        num_instances_available = BookInstance.objects.filter(status__exact='a').count()
        num_autors = Autor.objects.count()
        return render(request,'catalog/home.html',{'num_books':num_books,
                                                   'num_instances':num_instances,
                                                   'num_instances_available':num_instances_available,
                                                   'num_autors':num_autors
                                                   }
                      )

class BookListView(View):
    def get(self,request):
        all_books = Book.objects.all()
        return render(request,'catalog/book_list.html',{'all_books':all_books})

class BookDetailsView(View):
    def get(self,request,id):
        book = Book.objects.get(id=id)
        books_instance=BookInstance.objects.filter(book__id=id)
        return render(request,'catalog/book_details.html',{'book':book,'books_instance':books_instance})