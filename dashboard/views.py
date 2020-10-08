from datetime import date

from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from django.views.generic.base import View

from catalog.models import Book, BookInstance, Autor

today_date = date.today()

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
