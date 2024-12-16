from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('books/create/', views.create_book, name='create_book'),  
    path('books/<int:book_id>/edit/', views.edit_book, name='edit_book'),  
    path('books/<int:book_id>/delete/', views.delete_book, name='delete_book'),  
    path('about/', views.about_us, name='about_us'),
    path('books/<int:book_id>/archive/', views.archive_book, name='archive_book'),
    path('archived_books/', views.archived_books, name='archived_books'),
    path('archived_books/<int:book_id>/unarchive/', views.unarchive_book, name='unarchive_book'),
    path('archived_books/<int:book_id>/delete/', views.delete_book, name='delete_book_permanently'),
]
