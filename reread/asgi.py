'''
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat_sys.routing import websocket_urlpatterns  # Import your WebSocket routes

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

# This combines HTTP and WebSocket routing
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Regular Django HTTP requests
    "websocket": AuthMiddlewareStack(  # WebSocket connections
        URLRouter(
            websocket_urlpatterns  # Routes defined in chat_sys/routing.py
        )
    ),
})
'''
# reread/asgi.py

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import chat_sys.routing  # Update with your app name

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat_sys.routing.websocket_urlpatterns
        )
    ),
})