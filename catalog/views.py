from datetime import date

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.generic import ListView

from catalog.models import Book, BookInstance, Autor, BookHistoryRenting


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
        today_date = date.today()
        for i in update_book:
            i.status = 'r'
            i.reservation_time = today_date
            i.borrower = request.user
            i.save()
            book_history = BookHistoryRenting()
            book_history.book_instance = i.id
            book_history.borrower = i.borrower
            book_history.status = 'r'
            book_history.time_stamp = today_date
            book_history.save()



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
        today_date = date.today()
        return render(request, 'catalog/my_books.html',{'book_instance_borrower':book_instance_borrower,
                                                        'today_date':today_date})

class AuthorBooksView(View):
    def get(self, request, autor_slug=None):
        autor_books = Book.objects.all()
        if autor_slug:
            autor = Autor.objects.get(slug=autor_slug)
            autor_books = autor_books.filter(autor=autor)
            paginator = Paginator(autor_books, 5)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        return render(request, 'catalog/author.html',
                      {'autor_books': autor_books, 'autor': autor, 'page_obj': page_obj})

class UserBookHistoryView(View):
    def get(self,request):
        book_history = BookHistoryRenting.objects.filter(borrower=request.user)
        return render(request, 'dashboard/book_history.html', {'book_history': book_history})