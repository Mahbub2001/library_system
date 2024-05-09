from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import FormView
from . forms import UserRegistrationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import View
from transactions.models import BorrowBook
from transactions.views import send_transaction_email

class UserRegistrationView(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    
class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    success_url = reverse_lazy('homepage')
    

class UserLogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('homepage')
    
@login_required
def borrowed_books( request):
    books = BorrowBook.objects.filter(user = request.user.account)
    return render(request, 'accounts/profile.html',  {'books': books})
   
@login_required
def return_book(request, id):
    book_obj = get_object_or_404(BorrowBook, id=id, user=request.user.account)
    return_amount = book_obj.transactions.amount

    update_user_balance(book_obj.user, return_amount)
    send_return_email(book_obj.user.user, return_amount)
    delete_book_object(book_obj)

    notify_success(request)
    return redirect('profile')

def update_user_balance(user_account, amount):
    user_account.balance += amount
    user_account.save()

def send_return_email(user, amount):
    send_transaction_email(user, amount, "Book Return Message", "transactions/payment_email.html")

def delete_book_object(book_obj):
    book_obj.delete()

def notify_success(request):
    messages.success(request, 'Book returned successfully. Check Email')