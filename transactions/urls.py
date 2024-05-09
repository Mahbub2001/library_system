from django.urls import path
from . import views
urlpatterns = [
    path('deposite/', views.DepositMoneyView.as_view(), name = 'deposite' ),
    path('book_borrow/<int:id>', views.BorrowBookView.as_view(), name = 'book_borrow' ),
]
