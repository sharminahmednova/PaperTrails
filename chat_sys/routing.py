from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<other_user_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
    #re_path(r'ws/chat/(?P<other_user_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
    #re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
]