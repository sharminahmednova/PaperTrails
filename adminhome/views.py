from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, ReviewHistory
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render

from django.contrib.auth.decorators import login_required, user_passes_test


@login_required
@user_passes_test(lambda u: u.is_staff)
def AdminProfile(request):
    return render(request, 'adminhomehtml/admin_profile.html')


from django.db.models import Q

def home(request):
    query = request.GET.get('q', '')  # Get search query from URL params
    books = Book.objects.filter(status='pending')

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(description__icontains=query)
        )

    return render(request, 'adminhomehtml/homepage.html', {
        'books': books,
        'search_query': query
    })

def approve_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.status = 'approved'
    book.reviewed_at = timezone.now()
    book.save()
    ReviewHistory.objects.create(book=book, reviewer=request.user, action='approved')
    messages.success(request, f'"{book.title}" has been approved.')
    return redirect('homeadmin')

def reject_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.status = 'rejected'
    book.reviewed_at = timezone.now()
    book.save()
    ReviewHistory.objects.create(book=book, reviewer=request.user, action='rejected')
    messages.error(request, f'"{book.title}" has been marked as rejected.')
    return redirect('homeadmin')

def history(request):
    records = ReviewHistory.objects.select_related('book', 'reviewer').order_by('-timestamp')
    return render(request, 'adminhomehtml/history.html', {'records': records})



#-------------------------------------------------------
from django.http import JsonResponse

def get_books(request):
    # Get all books (you can filter if needed, e.g., only approved books)
    books = Book.objects.all()

    # Convert books to a list of dictionaries
    books_list = [
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "description": book.description,
            "price": str(book.price),  # Convert Decimal to string for JSON serialization
            "status": book.status,
            "posted_by": book.posted_by.username if book.posted_by else None,
            "reviewed_at": book.reviewed_at.isoformat() if book.reviewed_at else None,
            "posted_at": book.posted_at.isoformat() if book.posted_at else None,
        }
        for book in books
    ]

    # Return the books as a JSON response
    return JsonResponse(books_list, safe=False)  # safe=False allows a list as the response
