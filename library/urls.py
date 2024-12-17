from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('library.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# library/urls.py

from django.urls import path
from django.contrib.auth.decorators import login_required
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
    path('archived_books/<int:book_id>/delete/', views.delete_book_permanently, name='delete_book_permanently'),
]

# library/views.py
@login_required
def book_list(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    year = request.GET.get('year', '')

    books = Book.objects.filter(is_archived=False)

    if query:
        books = books.filter(title__icontains=query)
    if category:
        books = books.filter(category=category)
    if year:
        books = books.filter(year=year)

    categories = Book.objects.values_list('category', flat=True).distinct()
    years = Book.objects.values_list('year', flat=True).distinct()

    return render(request, 'book_list.html', {
        'books': books,
        'query': query,
        'category': category,
        'year': year,
        'categories': categories,
        'years': years,
    })

# book_library/settings.py

# Add these lines at the end of the file
LOGIN_REDIRECT_URL = 'book_list'
LOGOUT_REDIRECT_URL = 'login'
