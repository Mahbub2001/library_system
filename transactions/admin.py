from django.contrib import admin
from . models import Transaction, BorrowBook
# Register your models here.
admin.site.register(Transaction)
admin.site.register(BorrowBook)