from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Book

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
    if query:
        books = Book.objects.filter(title__icontains=query, is_archived=False)  # Exclude archived books
    else:
        books = Book.objects.filter(is_archived=False)  # Show only non-archived books
    return render(request, 'book_list.html', {'books': books, 'query': query})



# Book Detail View
@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id, is_archived=False)  # Ensure book is not archived
    return render(request, 'book_detail.html', {'book': book})


# Create Book (Admin only)
@login_required
@user_passes_test(is_admin)
def create_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        summary = request.POST['summary']
        Book.objects.create(title=title, author=author, summary=summary)
        return redirect('book_list')

    return render(request, 'create_book.html')

# Edit Book (Admin only)
@login_required
@user_passes_test(is_admin)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        book.title = request.POST['title']
        book.author = request.POST['author']
        book.summary = request.POST['summary']
        book.save()
        return redirect('book_detail', book_id=book.id)

    return render(request, 'edit_book.html', {'book': book})


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
    books = Book.objects.filter(is_archived=True)
    return render(request, 'archived_books.html', {'books': books})


# Unarchived Book (Admin only)
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

def about_us(request):
    return render(request, 'about_us.html')

