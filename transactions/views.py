from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, View
from . forms import DepositForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from . models import Transaction, BorrowBook
from books.models import Books


def send_transaction_email(user, amount, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()


class DepositMoneyView(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transaction_form.html'
    model = Transaction
    form_class = DepositForm

    success_url = reverse_lazy('homepage')
    def get_initial(self):
        initial = {'transaction_type': 1}
        return initial
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs
    def form_valid(self, form): 
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account 
        account.balance += amount 
        account.save(
            update_fields=[
                'balance'
            ]
        )
        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ is deposited to your account successfully'
        )
        send_transaction_email(self.request.user, amount, "Deposite Message", "transactions/deposite_email.html")
        return super().form_valid(form)



class BorrowBookView(LoginRequiredMixin, View):
    success_url = reverse_lazy('profile')
    pk_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        book_id = kwargs.get(self.pk_url_kwarg)
        book = Books.objects.filter(id=book_id).first()
        if not book:
            return redirect('homepage')
        return self.handle_borrow_request(request, book)

    def handle_borrow_request(self, request, book):
        price = book.book_price
        account = request.user.account

        if account.balance < price:
            return self.handle_insufficient_balance(request, book)

        return self.borrow_book(request, book, account, price)

    def handle_insufficient_balance(self, request, book):
        messages.warning(request, 'You do not have sufficient balance')
        return redirect('book_details', id=book.id)

    def borrow_book(self, request, book, account, price):
        account.balance -= price
        transaction = Transaction.objects.create(account=account, amount=price, balance_after_transaction=account.balance,
            transaction_type=2)
        BorrowBook.objects.create(user=account, book=book, transactions=transaction)
        account.save(update_fields=['balance'])
        messages.success(request, f'You borrowed the book with {"{:,.2f}".format(float(price))}tk. Check email')
        send_transaction_email(request.user, price, "Book Borrow Message", "transactions/borrow_email.html")
        return redirect(self.success_url)
    


