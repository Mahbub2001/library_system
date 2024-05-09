from django import forms
from . models import UserReviews


class CommentForm(forms.ModelForm):
    class Meta: 
        model = UserReviews
        fields = ['name', 'email', 'body']
