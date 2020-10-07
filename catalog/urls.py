
from django.contrib import admin
from django.urls import path

from catalog.views import HomePageView, BookListView, BookDetailsView, SearchView, BookReservations, MyBooksView, AuthorBooksView

urlpatterns = [
    path('', HomePageView.as_view(),name='home'),
    path('books/', BookListView.as_view(),name='all_books'),
    path('books/<int:id>/', BookDetailsView.as_view(),name='book_details'),
    path('search/', SearchView.as_view(), name='search'),
    path('reservation/<uuid:id>/', BookReservations.as_view(),name='book_reservation'),
    path('my_books/', MyBooksView.as_view(),name='my_books'),
    path('author/<slug:autor_slug>/', AuthorBooksView.as_view(),name='author'),
]

