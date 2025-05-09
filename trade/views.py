from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from adminhome.models import Book
from .models import TradeRequest
from notifications.models import Notification
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

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

# 🚀 Fixed this View for AJAX (Frontend)
@require_POST
@login_required
def send_trade_request(request):
    offered_book_id = request.POST.get('offered_book_id')
    requested_book_id = request.POST.get('requested_book_id')

    if not offered_book_id or not requested_book_id:
        return JsonResponse({'success': False, 'message': 'Invalid book selection.'}, status=400)

    try:
        offered_book = get_object_or_404(Book, id=offered_book_id)
        requested_book = get_object_or_404(Book, id=requested_book_id)

        if not requested_book.posted_by:
            return JsonResponse({'success': False, 'message': 'The requested book has no owner.'}, status=400)

        existing_request = TradeRequest.objects.filter(
            sender=request.user,
            receiver=requested_book.posted_by,
            offered_book=offered_book,
            requested_book=requested_book,
            status='pending'
        ).first()

        if existing_request:
            return JsonResponse({'success': False, 'message': 'You have already sent a trade request for this book.'})

        trade_request = TradeRequest.objects.create(
            sender=request.user,
            receiver=requested_book.posted_by,
            offered_book=offered_book,
            requested_book=requested_book,
            status='pending'
        )

        # Send notification
        Notification.objects.create(
            user=requested_book.posted_by,
            message=f"{request.user.username} sent you a trade request for '{requested_book.title}'."
        )

        return JsonResponse({'success': True, 'message': 'Trade request sent!'})

    except Exception as e:
        print(f"Error creating trade request: {str(e)}")
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=500)

@login_required
def trade_history(request):
    user = request.user
    sent_requests = TradeRequest.objects.filter(sender=user).order_by('-timestamp')
    received_requests = TradeRequest.objects.filter(receiver=user).order_by('-timestamp')

    return render(request, 'trade/trade_history.html', {
        'sent_requests': sent_requests,
        'received_requests': received_requests,
    })

@login_required
def get_trade_requests(request):
    sender = request.user
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

@require_POST
@login_required
def accept_trade_request(request, trade_id):
    trade_request = get_object_or_404(TradeRequest, id=trade_id, receiver=request.user)

    if trade_request.status == 'pending':
        trade_request.status = 'accepted'
        trade_request.save()

        Notification.objects.create(
            user=trade_request.sender,
            message=f"Your trade request for '{trade_request.requested_book.title}' has been accepted!"
        )

        return JsonResponse({'success': True, 'new_status': 'accepted', 'message': 'Trade accepted successfully.'})

    return JsonResponse({'success': False})

@require_POST
@login_required
def decline_trade_request(request, trade_id):
    trade_request = get_object_or_404(TradeRequest, id=trade_id, receiver=request.user)

    if trade_request.status == 'pending':
        trade_request.status = 'declined'
        trade_request.save()

        Notification.objects.create(
            user=trade_request.sender,
            message=f"Your trade request for '{trade_request.requested_book.title}' has been declined."
        )

        return JsonResponse({'success': True, 'new_status': 'declined', 'message': 'Trade declined successfully.'})

    return JsonResponse({'success': False})
