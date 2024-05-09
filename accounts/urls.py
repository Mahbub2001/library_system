from django.urls import path
from . import views
urlpatterns = [
    path('profile/', views.borrowed_books, name= 'profile'),
    path('login/', views.UserLoginView.as_view(), name= 'login'),
    path('register/', views.UserRegistrationView.as_view(), name= 'register'),
    path('logout/', views.UserLogoutView.as_view(), name= 'logout'),
    path('return_book/<int:id>', views.return_book, name= 'return_book'),
]
