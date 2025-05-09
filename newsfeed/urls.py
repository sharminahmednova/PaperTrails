from django.urls import path

from newsfeed import views
from .views import wall
from .views import chat_with_user
urlpatterns = [
    path('', wall, name='wall'),
    path('', views.wall, name='newsfeed_wall'),
    path('notifications/read/', views.mark_all_read, name='mark_all_read'),
    path('notification/', views.notifications, name='notifications'),
    path('wall/notification/', views.notifications, name='notifications'),
    path('wall/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('review/<int:user_id>/', views.add_review, name='add_review'),
    path('reviews/<int:user_id>/', views.user_reviews, name='user_reviews'),
    path('chat/<int:user_id>/', views.chat_with_user, name='chat_with_user'),
    path('api/chat/conversations/', views.chat_conversations, name='chat_conversations'),
    path('notification/', views.notification_list, name='notifications'),
    path('search-users/', views.search_users, name='search_users'),
]
