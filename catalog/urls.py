
from django.contrib import admin
from django.urls import path

from catalog.views import HomePageView, BookListView, BookDetailsView, SearchView

urlpatterns = [
    path('', HomePageView.as_view(),name='home'),
    path('books/', BookListView.as_view(),name='all_books'),
    path('books/<int:id>/', BookDetailsView.as_view(),name='book_details'),
    path('search/', SearchView.as_view(), name='search'),
]