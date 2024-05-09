from django.db import models
from categories.models import Category
# Create your models here.
class Books(models.Model):
    category = models.ManyToManyField(Category)
    title = models.CharField(max_length=100)
    description = models.TextField()
    borrow_date = models.DateTimeField(auto_now_add = True)
    image = models.ImageField(upload_to='uploads/', blank = True, null = True)
    book_price = models.IntegerField()
    

    def __str__(self):
        return self.title


class UserReviews(models.Model):
    review = models.ForeignKey(Books, on_delete = models.CASCADE, related_name='reviews')
    name = models.CharField(max_length = 100)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"comments by {self.name}"

