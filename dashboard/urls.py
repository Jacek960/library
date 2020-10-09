from django.urls import path

from dashboard.views import DashboardView, BookOnReservationView, BookOnLoanView, BookRentView, BookReturnView

urlpatterns = [
    path('', DashboardView.as_view(),name='dashboard'),
    path('reserv/', BookOnReservationView.as_view(),name='book_on_reservtion'),
    path('loan/', BookOnLoanView.as_view(),name='book_on_loan'),
    path('loan/<uuid:id>/', BookRentView.as_view(),name='book_rent'),
    path('return/<uuid:id>/', BookReturnView.as_view(),name='book_return'),

]
