from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from adminhome.models import Book
from .models import TradeRequest
from notifications.models import Notification
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
import logging

# Set up logging
logger = logging.getLogger(__name__)

@login_required
def trade_center(request):
    user = request.user
    query = request.GET.get('q', '')

    user_books = Book.objects.filter(posted_by=user, status='approved')
    matched_books = []

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
        offered_book_id = request.POST.get('offered_book_id')
        requested_book_id = request.POST.get('requested_book_id')

        if not offered_book_id or not requested_book_id:
            return JsonResponse({'success': False, 'message': 'Invalid book selection.'}, status=400)

        try:
            offered_book = get_object_or_404(Book, id=offered_book_id)
            requested_book = get_object_or_404(Book, id=requested_book_id)

            if not requested_book.posted_by:
                return JsonResponse({'success': False, 'message': 'The requested book has no owner.'}, status=400)

            # Check if a trade request already exists
            existing_request = TradeRequest.objects.filter(
                sender=request.user,
                offered_book=offered_book,
                requested_book=requested_book
            ).exists()

            if existing_request:
                return JsonResponse({'success': False, 'message': 'Trade request sent already!'}, status=400)

            # Create the trade request
            trade_request = TradeRequest.objects.create(
                sender=request.user,
                receiver=requested_book.posted_by,
                offered_book=offered_book,
                requested_book=requested_book,
                status='pending'
            )

            # Create a notification for the receiver
            Notification.objects.create(
                user=requested_book.posted_by,
                message=f"{request.user.username} sent you a trade request for '{requested_book.title}'"
            )

            return JsonResponse({'success': True, 'message': 'Trade request sent successfully!'})

        except Exception as e:
            logger.error(f"Error in send_trade_request: {str(e)}")
            return JsonResponse({'success': False, 'message': f'Failed to send trade request: {str(e)}'}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)

@login_required
def trade_history(request):
    user = request.user
    sent_requests = TradeRequest.objects.filter(sender=user).order_by('-timestamp')
    received_requests = TradeRequest.objects.filter(receiver=user).order_by('-timestamp')

    if request.method == 'POST':
        trade_id = request.POST.get('trade_id')
        action = request.POST.get('action')
        trade_request = get_object_or_404(TradeRequest, id=trade_id)

        # Handle AJAX requests
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if trade_request.sender == user and action == 'cancel' and trade_request.status == 'pending':
                trade_request.delete()
                return JsonResponse({'success': True, 'message': 'Trade request cancelled successfully!'})
            elif trade_request.receiver == user:
                if action in ['accept', 'decline'] and trade_request.status == 'pending':
                    trade_request.status = action + 'ed'  # 'accepted' or 'declined'
                    trade_request.save()
                    Notification.objects.create(
                        user=trade_request.sender,
                        message=f"Your trade request for '{trade_request.requested_book.title}' has been {trade_request.status} by {user.username}"
                    )
                    return JsonResponse({'success': True, 'message': f'Trade request {trade_request.status} successfully!', 'status': trade_request.status})
                elif action == 'cart' and trade_request.status == 'accepted':
                    return JsonResponse({'success': True, 'message': 'Add to cart functionality to be implemented'})
            return JsonResponse({'success': False, 'message': 'Invalid request.'}, status=400)

        # Handle regular POST requests
        if trade_request.sender == user and action == 'cancel' and trade_request.status == 'pending':
            trade_request.delete()
            messages.success(request, "Trade request cancelled successfully!")
        elif trade_request.receiver == user:
            if action == 'accept':
                trade_request.status = 'accepted'
                Notification.objects.create(
                    user=trade_request.sender,
                    message=f"Your trade request for '{trade_request.requested_book.title}' has been accepted by {user.username}"
                )
            elif action == 'decline':
                trade_request.status = 'declined'
                Notification.objects.create(
                    user=trade_request.sender,
                    message=f"Your trade request for '{trade_request.requested_book.title}' has been declined by {user.username}"
                )
            elif action == 'cart' and trade_request.status == 'accepted':
                messages.info(request, "Add to cart functionality to be implemented")
            trade_request.save()
        return redirect('tradehistory')

    return render(request, 'trade/trade_history.html', {
        'sent_requests': sent_requests,
        'received_requests': received_requests,
    })

def get_trade_requests(request):
    sender_id = request.user.id
    try:
        sender = User.objects.get(id=sender_id)
    except User.DoesNotExist:
        return JsonResponse({"error": f"User with ID '{sender_id}' not found"}, status=404)

    sent_requests = TradeRequest.objects.filter(sender=sender).order_by('-timestamp')
    trade_requests_list = [
        {
            "id": str(trade.id),
            "name": f"{trade.sender.username} to {trade.receiver.username}",
            "class": trade.status
        }
        for trade in sent_requests
    ]

    return JsonResponse(trade_requests_list, safe=False)