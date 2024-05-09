from django.db import models
from accounts.models import UserAccount
from books.models import Books
from . constants import TRANSACTION_TYPE
# Create your models here.

class Transaction(models.Model):
    account = models.ForeignKey(UserAccount, related_name = 'transactions', on_delete = models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits = 12)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits = 12)
    timestamp = models.DateTimeField(auto_now_add=True) 
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE, null = True)
    
    class Meta:
        ordering = ['timestamp'] 

    def __str__(self):
        return str(self.account)
    

class BorrowBook(models.Model):
    user = models.ForeignKey(UserAccount, on_delete = models.CASCADE)
    book = models.ForeignKey(Books, on_delete = models.CASCADE)
    transactions = models.ForeignKey(Transaction, on_delete = models.CASCADE)

    
    def __str__(self):
        return str(self.user)