from datetime import timedelta, timezone
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Message
from django.contrib.auth.decorators import login_required

from chat_sys import models
User = get_user_model()
# In your chat_sys/views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message

@login_required
def conversation_list(request):
    # Get all conversations where the current user is a participant
    conversations = Conversation.objects.filter(participants=request.user).prefetch_related('participants', 'messages')
    
    data = []
    for conv in conversations:
        # Get the other participant (assuming 1-on-1 chats)
        other_user = conv.participants.exclude(id=request.user.id).first()
        last_message = conv.messages.order_by('-timestamp').first()
        
        data.append({
            'id': conv.id,
            'other_user': {
                'id': other_user.id if other_user else None,
                'username': other_user.username if other_user else 'Unknown',
            },
            'unread_count': conv.messages.filter(sender=other_user, read=False).count() if other_user else 0,
            'last_message': {
                'content': last_message.content if last_message else '',
                'timestamp': last_message.timestamp.isoformat() if last_message else '',
            }
        })
    
    return JsonResponse(data, safe=False)

def chat_view(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')
    
    # Mark received messages as read
    messages.filter(receiver=request.user, is_read=False).update(is_read=True)
    
    return render(request, 'chat_sys/chat.html', {
        'other_user': other_user,
        'messages': messages
    })
'''
@login_required
def chat_conversations(request):
    # Get last 24 hours of messages
    recent_messages = Message.objects.filter(
        models.Q(sender=request.user) | models.Q(receiver=request.user),
        timestamp__gte=timezone.now() - timedelta(hours=24)
    ).order_by('-timestamp')
    
    # Group by user
    conversations = {}
    for msg in recent_messages:
        other_user = msg.sender if msg.sender != request.user else msg.receiver
        if other_user.id not in conversations:
            conversations[other_user.id] = {
                'user': {
                    'id': other_user.id,
                    'username': other_user.username
                },
                'last_message': msg.text[:50] + ('...' if len(msg.text) > 50 else ''),
                'last_message_time': msg.timestamp.strftime("%H:%M"),
                'unread': msg.receiver == request.user and not msg.is_read
            }
    
    return JsonResponse({
        'conversations': list(conversations.values()),
        'unread_count': Message.objects.filter(
            receiver=request.user,
            is_read=False
        ).count()
    })
'''
from newsfeed.models import Notification

@login_required
def send_message(request):
    if request.method == 'POST':
        sender = request.user
        receiver_id = request.POST.get('receiver_id')
        message_text = request.POST.get('message')

        receiver = User.objects.get(id=receiver_id)

        # Save message
        Message.objects.create(sender=sender, receiver=receiver, text=message_text)

        # Create notification
        Notification.objects.create(
            recipient=receiver,
            message=f"{sender.username} sent you a new message."
        )

        return JsonResponse({'status': 'Message sent & notification created!'})
