from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.http import JsonResponse

@login_required

def notifications_list(request):
    notifications = Notification.objects.filter(user=request.user)
    notifications.update(is_read=True)  # Mark as read when viewed
    return render(request, 'notifications_list.html', {'notifications': notifications})

@login_required
def mark_as_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False}, status=404)
