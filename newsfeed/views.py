
from datetime import timezone
from django.shortcuts import render, redirect
from .models import Notification, Post, Query
from .forms import PostForm, ReplyForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Query, Notification
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Review
from .forms import ReviewForm
from django.db.models import Avg

@login_required
def user_reviews(request, user_id):
    reviewed_user = get_object_or_404(User, id=user_id)
    reviews = Review.objects.filter(reviewed_user=reviewed_user).order_by('-created_at')
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    return render(request, 'newsfeed/user_reviews.html', {
        'reviewed_user': reviewed_user,
        'reviews': reviews,
        'average_rating': average_rating,
    })
@login_required
def add_review(request, user_id):
    reviewed_user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.reviewed_user = reviewed_user
            review.save()
            return redirect('wall')  # after review submitted, go back to wall
    else:
        form = ReviewForm()

    return render(request, 'newsfeed/add_review.html', {
        'form': form,
        'reviewed_user': reviewed_user,
    })


@login_required
def wall(request):
    if request.method == 'POST':
        if 'reply_query_id' in request.POST:
            # It's a reply
            query = Query.objects.get(id=request.POST['reply_query_id'])
            form = ReplyForm(request.POST)
            if form.is_valid():
                reply = form.save(commit=False)
                reply.user = request.user
                reply.query = query
                reply.save()
                return redirect('newsfeed_wall')
        else:
            # It's a new post
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                new_query = form.save(commit=False)
                new_query.user = request.user
                new_query.save()
                other_users = User.objects.exclude(id=request.user.id)
                for user in other_users:
                    Notification.objects.create(
                        recipient=user,
                        message=f"{request.user.username} posted a new query: {new_query.text[:50]}"
                    )
                return redirect('newsfeed_wall')
    else:
        form = PostForm()

    reply_form = ReplyForm()
    queries = Query.objects.all().order_by('-created_at')
    unread_notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-created_at')

    return render(request, 'newsfeed/wall.html', {
        'form': form,
        'queries': queries,
        'reply_form': reply_form,
        'notifications': unread_notifications,
    })
'''
def wall(request):
    if request.method == 'POST':
        text = request.POST.get('query_text')
        image = request.FILES.get('query_image')  # <-- Get uploaded image

        if text or image:
            new_query = Query.objects.create(
                user=request.user,
                text=text,
                image=image
            )

            # Notify other users
            other_users = User.objects.exclude(id=request.user.id)
            for user in other_users:
                Notification.objects.create(
                    recipient=user,
                    message=f"{request.user.username} posted a new query: {new_query.text[:50]}"
                )
            return redirect('newsfeed_wall')

    queries = Query.objects.all().order_by('-created_at')
    unread_notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-created_at')

    return render(request, 'newsfeed/wall.html', {
        'queries': queries,
        'notifications': unread_notifications
    })
'''
@login_required
def mark_all_read(request):
    request.user.notifications.update(is_read=True)
    return redirect('newsfeed_wall')
@login_required
def notifications(request):
    user_notifications = request.user.notifications.order_by('-created_at')
    print(user_notifications)  # Debugging line to check notifications
    return render(request, 'newsfeed/notification.html', {
        'notifications': user_notifications
    })

def create_notification(recipient, message):
    Notification.objects.create(
        recipient=recipient,
        message=message,
        created_at=timezone.now(),
        is_read=False
    )
def mark_as_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    notification.is_read = True
    notification.save()
    return redirect('notifications')
@login_required


def delete_post(request, post_id):
    post = get_object_or_404(Query, id=post_id)
    if post.user == request.user:
        post.delete()
    return redirect('wall')
  # Redirect back to the notifications page
# Create your views here.
