from django.shortcuts import render
from books.models import Category, Books

def home(request, id=None):
    cat = Category.objects.all()
    books = Books.objects.filter(category__id=id) if id else Books.objects.all()
    print(books)
    return render(request, 'index.html', {'cat': cat, 'books': books })
