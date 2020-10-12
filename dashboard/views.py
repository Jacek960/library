from datetime import date, timedelta

from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from django.views.generic.base import View

from catalog.models import Book, BookInstance, Autor, BookHistoryRenting


class DashboardView(View):
    def get(self,request):
        if request.user.is_staff:
            num_books = Book.objects.all().count()
            num_instances = BookInstance.objects.all().count()
            num_instances_available = BookInstance.objects.filter(status__exact='a').count()
            num_autors = Autor.objects.count()
            active_users = User.objects.all()[0:11]
            instances_reserved = BookInstance.objects.filter(status__exact='r')[0:11]
            instances_on_loan = BookInstance.objects.filter(status__exact='o').order_by('due_back')[0:11]
            today_date = date.today()
            return render(request,'dashboard/dashboard.html',{
                'num_books':num_books,
                'num_instances':num_instances,
                'num_instances_available':num_instances_available,
                'num_autors':num_autors,
                'active_users':active_users,
                'instances_reserved':instances_reserved,
                'instances_on_loan':instances_on_loan,
                'today_date':today_date,
            } )
        else:
            return redirect('/')

class BookOnReservationView(View):
    def get(self,request):
        if request.user.is_staff:
            book_reserved = BookInstance.objects.filter(status__exact='r')
            return render(request,'dashboard/book_reservation.html',{'book_reserved':book_reserved})
        else:
            return redirect('/')


class BookOnLoanView(View):
    def get(self,request):
        if request.user.is_staff:
            book_on_loan = BookInstance.objects.filter(status__exact='o')
            today_date = date.today()
            return render(request,'dashboard/book_on_loan.html',{'book_on_loan':book_on_loan,
                                                                 'today_date':today_date,
                                                                 })
        else:
            return redirect('/')

class BookRentView(View):
    def get(self,request,id):
        book_instance_rent = BookInstance.objects.filter(id=id)
        return render(request, 'dashboard/book_rent.html', {'book_instance_rent':book_instance_rent})
    def post(self,request,id):
        update_book = BookInstance.objects.filter(id=id)
        today_date = date.today()
        for i in update_book:
            i.status = 'o'
            i.reservation_time = None
            i.due_back = today_date + timedelta(days=14)
            i.save()
            book_history = BookHistoryRenting()
            book_history.book_instance = i.id
            book_history.borrower = i.borrower
            book_history.status = 'o'
            book_history.time_stamp = today_date
            book_history.save()
        return redirect('/dashboard/')

class BookReturnView(View):
    def get(self,request,id):
        book_instance_rent = BookInstance.objects.filter(id=id)
        return render(request, 'dashboard/book_return.html', {'book_instance_rent':book_instance_rent})
    def post(self,request,id):
        update_book = BookInstance.objects.filter(id=id)
        today_date = date.today()
        for i in update_book:
            i.status = 'a'
            i.due_back = None
            i.borrower = None
            i.save()
            book_history = BookHistoryRenting()
            book_history.book_instance = i.id
            book_history.borrower = None
            book_history.status = 'a'
            book_history.time_stamp = today_date
            book_history.save()
        return redirect('/dashboard/')

class HistoryView(View):
    def get(self,request,book_instance):
        books = BookInstance.objects.filter(id=book_instance)
        book_history = BookHistoryRenting.objects.filter(book_instance=book_instance)
        return render(request, 'dashboard/book_history.html', {'book_history': book_history,'books':books})



