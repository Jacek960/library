from django.db.models import Q
from django.shortcuts import render, redirect

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
        num_instances_available = BookInstance.objects.filter(book__id=id,status__exact='a').count()
        books_instance_all = BookInstance.objects.filter(book__id=id).count()
        return render(request,'catalog/book_details.html',{'book':book,
                                                           'books_instance':books_instance,
                                                           'num_instances_available':num_instances_available,
                                                           'books_instance_all':books_instance_all})

class BookReservations(View):
    def get(self,request,id):
        book_instance_reservation = BookInstance.objects.filter(id=id)
        for i in book_instance_reservation:
            if i.status != 'a':
                return redirect('/')
            else:
                return render(request, 'catalog/book_reservation.html', {'book_instance_reservation':book_instance_reservation})
    def post(self,request,id):
        update_book = BookInstance.objects.filter(id=id)
        for i in update_book:
            i.status = 'r'
            i.borrower = request.user
            i.save()
        return redirect('/')


class SearchView(View):
    def get(self, request):
        books = None
        query = None
        if 'q' in request.GET:
            query = request.GET.get('q')
            if query == '':
                return redirect('/search/?q=""')
            else:
                books = Book.objects.all().filter(
                    Q(title__icontains=query) | Q(autor__name__icontains=query))
        return render(request, 'catalog/search.html', {'query': query, 'books': books})

class MyBooksView(View):
    def get(self,request):
        book_instance_borrower = BookInstance.objects.filter(borrower=request.user)
        return render(request, 'catalog/my_books.html',{'book_instance_borrower':book_instance_borrower})