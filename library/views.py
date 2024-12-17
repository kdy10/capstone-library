from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Book
from django.core.paginator import Paginator
from .forms import BookForm

# Check if the user is an admin
def is_admin(user):
    return user.is_staff

# Register View
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
     
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')  
 
    return render(request, 'register.html')

# Login View
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)  
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('book_list')  
            else:
                messages.error(request, "Invalid email or password")
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
    
    return render(request, 'login.html')

# Home View (Redirect to login or book list)
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return redirect('book_list')

# Book List View
@login_required
def book_list(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    year = request.GET.get('year', '')
    page_number = request.GET.get('page', 1)

    books = Book.objects.filter(is_archived=False)

    if query:
        books = books.filter(title__icontains=query)
    if category:
        books = books.filter(category=category)
    if year:
        books = books.filter(year=year)

    categories = Book.objects.values_list('category', flat=True).distinct()
    years = Book.objects.values_list('year', flat=True).distinct()

    paginator = Paginator(books, 10)  # Show 10 books per page
    page_obj = paginator.get_page(page_number)

    return render(request, 'book_list.html', {
        'page_obj': page_obj,
        'query': query,
        'category': category,
        'year': year,
        'categories': categories,
        'years': years,
    })


# Book Detail View
@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book_detail.html', {'book': book})


# Create Book (Admin only)
@login_required
@user_passes_test(is_admin)
def create_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        summary = request.POST['summary']
        category = request.POST['category']
        year = request.POST['year']
        attachment = request.FILES.get('attachment')

        Book.objects.create(title=title, author=author, summary=summary, category=category, year=year, attachment=attachment)
        return redirect('book_list')

    return render(request, 'create_book.html')

# Edit Book (Admin only)
@login_required
@user_passes_test(is_admin)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', book_id=book.id)
    else:
        form = BookForm(instance=book)

    return render(request, 'edit_book.html', {'form': form})


# Archive Book (Admin only)
@login_required
@user_passes_test(is_admin)
def archive_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.is_archived = True
    book.save()
    return redirect('book_list')

# View Archived Book (Admin only)
@login_required
@user_passes_test(is_admin)
def archived_books(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    year = request.GET.get('year', '')
    page_number = request.GET.get('page', 1)

    books = Book.objects.filter(is_archived=True)

    if query:
        books = books.filter(title__icontains=query)
    if category:
        books = books.filter(category=category)
    if year:
        books = books.filter(year=year)

    categories = Book.objects.values_list('category', flat=True).distinct()
    years = Book.objects.values_list('year', flat=True).distinct()

    paginator = Paginator(books, 10)  # Show 10 books per page
    page_obj = paginator.get_page(page_number)

    return render(request, 'archived_books.html', {
        'page_obj': page_obj,
        'query': query,
        'category': category,
        'year': year,
        'categories': categories,
        'years': years,
    })


# Unarchive Book (Admin only)
@login_required
@user_passes_test(is_admin)
def unarchive_book(request, book_id):
    book = get_object_or_404(Book, id=book_id, is_archived=True)
    book.is_archived = False
    book.save()
    return redirect('archived_books')

# Delete Book (Admin only)
@login_required
@user_passes_test(is_admin)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id, is_archived=True)
    book.delete()
    return redirect('archived_books')

# Delete Book Permanently (Admin only)
@login_required
@user_passes_test(is_admin)
def delete_book_permanently(request, book_id):
    book = get_object_or_404(Book, id=book_id, is_archived=True)
    book.delete()
    return redirect('archived_books')

def about_us(request):
    return render(request, 'about_us.html')
