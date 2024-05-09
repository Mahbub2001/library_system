from django.shortcuts import render, redirect
from . models import Books
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . forms import CommentForm
from transactions.models import BorrowBook
from django.core.exceptions import ValidationError

class DetailBookView(DetailView):
    model = Books
    pk_url_kwarg = 'id'
    template_name = 'books/book_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = self.object.reviews.all()
        context['review_form'] = CommentForm()
        context['reviews'] = reviews
        context['book'] = Books.objects.get(pk=self.kwargs['id'])
        return context     

    def post(self, request, *args, **kwargs):
        review_form = CommentForm(data=request.POST)
        book = self.get_object()
        user_account = request.user.account
        book_id = self.kwargs['id']
        if book.reviews.filter(email=request.user.email).exists():
            messages.warning(request, 'You have already reviewed this book.')
            return redirect('book_details', id=book_id)

        if BorrowBook.objects.filter(user=user_account, book=book).exists():
            if review_form.is_valid():
                name = review_form.cleaned_data['name']
                email = review_form.cleaned_data['email']
                
                if name != request.user.username or email != request.user.email:
                    messages.warning(request, 'Invalid username or email.')
                    return redirect('book_details', id=book_id)
                else:
                    try:
                        if book.reviews.filter(email=email).exists():
                            raise ValidationError('You have already reviewed this book.')

                        new_review = review_form.save(commit=False)
                        new_review.review = book
                        new_review.save()
                        messages.success(request, 'Review submitted successfully.')
                    except ValidationError as e:
                        messages.error(request, e.message)

        else:
            messages.warning(request, 'You have to borrow the book first before giving a review.')

        return redirect('book_details', id=book_id)
