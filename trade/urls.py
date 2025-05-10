from django.urls import path
from . import views
from user_authintication.views import ProfilePage

urlpatterns = [
    path('', views.trade_center, name='trade-center'),
    path('send-request/', views.send_trade_request, name='send_trade_request'),
    path('history/22101028/', views.trade_history, name='tradehistory'),
    path('profile/', ProfilePage, name='profile'),
    path('get_trade_requests/22101028/', views.get_trade_requests, name='get_trade_requests'),
]