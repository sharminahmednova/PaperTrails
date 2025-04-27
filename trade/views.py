from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from adminhome.models import Book
from .models import TradeRequest  # Ensure TradeRequest is imported
from notifications.models import Notification
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User  # Ens

@login_required
def trade_center(request):
    user = request.user
    query = request.GET.get('q', '')

    # Get only approved books posted by the current user
    user_books = Book.objects.filter(posted_by=user, status='approved')

    matched_books = []

    # For each user's approved book, find similar priced approved books from others
    for book in user_books:
        similar_books = Book.objects.filter(
            status='approved',
            price__gte=book.price - 10,
            price__lte=book.price + 10
        ).exclude(posted_by=user)

        if query:
            similar_books = similar_books.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(description__icontains=query)
            )

        similar_books = similar_books.order_by('posted_at')

        if similar_books.exists():
            matched_books.append({
                'user_book': book,
                'match': similar_books.first()
            })

    return render(request, 'trade/trade_page.html', {
        'matched_books': matched_books,
        'search_query': query,
    })

@login_required
def send_trade_request(request):
    if request.method == 'POST':
        # Debug: Print the form data to ensure IDs are being received
        offered_book_id = request.POST.get('offered_book_id')
        requested_book_id = request.POST.get('requested_book_id')
        print(f"Offered Book ID: {offered_book_id}, Requested Book ID: {requested_book_id}")

        # Validate the book IDs
        if not offered_book_id or not requested_book_id:
            messages.error(request, "Invalid book selection.")
            return redirect('trade-center')

        try:
            offered_book = get_object_or_404(Book, id=offered_book_id)
            requested_book = get_object_or_404(Book, id=requested_book_id)

            if not requested_book.posted_by:
                messages.error(request, "The requested book has no owner.")
                return redirect('trade-center')

            # Create the trade request
            trade_request = TradeRequest.objects.create(
                sender=request.user,
                receiver=requested_book.posted_by,
                offered_book=offered_book,
                requested_book=requested_book,
                status='pending'
            )
            # Add a success message to confirm TradeRequest creation
            messages.success(request, "Trade request created successfully.")

            # Create a notification for the receiver
            Notification.objects.create(
                user=requested_book.posted_by,
                message=f"{request.user.username} sent you a trade request for '{requested_book.title}'"
            )

            # Redirect to trade history with a success flag
            return redirect('tradehistory?request_sent=true')

        except Exception as e:
            # Log the error and show a message to the user
            print(f"Error creating trade request: {str(e)}")
            messages.error(request, f"Failed to send trade request: {str(e)}")
            return redirect('trade-center')

    return redirect('trade-center')

@login_required
def trade_history(request):
    user = request.user
    sent_requests = TradeRequest.objects.filter(sender=user).order_by('-timestamp')
    received_requests = TradeRequest.objects.filter(receiver=user).order_by('-timestamp')

    # Check for the query parameter to show the popup
    request_sent = request.GET.get('request_sent', 'false') == 'true'

    return render(request, 'trade/trade_history.html', {
        'sent_requests': sent_requests,
        'received_requests': received_requests,
        'request_sent': request_sent
    })



#--------------------------------------------------------------------------------------------------------------------------------
def get_trade_requests(request):
    # Hardcode the sender's user ID (replace 1 with your actual user ID)
    sender_id = 19  # Replace this with your actual user ID

    # Get the sender user object
    try:
        sender = User.objects.get(id=sender_id)
    except User.DoesNotExist:
        return JsonResponse({"error": f"User with ID '{sender_id}' not found"}, status=404)

    # Get trade requests where the specified user is the sender
    sent_requests = TradeRequest.objects.filter(sender=sender).order_by('-timestamp')

    # Convert trade requests to a list of dictionaries
    trade_requests_list = [
        {
            "id": str(trade.id),
            "name": f"{trade.sender.username} to {trade.receiver.username}",
            "class": trade.status
        }
        for trade in sent_requests
    ]

    return JsonResponse(trade_requests_list, safe=False)