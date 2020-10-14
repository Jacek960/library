from django.urls import path

from dashboard.views import DashboardView, BookOnReservationView, BookOnLoanView, BookRentView, BookReturnView, \
    HistoryView, BookCreateView, AuthorCreateView, CategoryCreateView, BookInstanceCreateView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('reserv/', BookOnReservationView.as_view(), name='book_on_reservtion'),
    path('loan/', BookOnLoanView.as_view(), name='book_on_loan'),
    path('loan/<uuid:id>/', BookRentView.as_view(), name='book_rent'),
    path('return/<uuid:id>/', BookReturnView.as_view(), name='book_return'),
    path('book_history/<str:book_instance>/', HistoryView.as_view(), name='book_history'),
    path('add_book/', BookCreateView.as_view(), name='add_book'),
    path('add_author/', AuthorCreateView.as_view(), name='add_author'),
    path('add_category/', CategoryCreateView.as_view(), name='add_category'),
    path('add_book_instance/', BookInstanceCreateView.as_view(), name='add_book_instance'),

]
