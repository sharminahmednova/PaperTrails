from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Message

User = get_user_model()

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