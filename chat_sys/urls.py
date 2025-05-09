from django.urls import path
from . import views

urlpatterns = [
    path('chat/<int:user_id>/', views.chat_view, name='chat'),
    path('chat/<uuid:other_user_id>/', views.chat_view, name='chat'),
    #path('api/conversations/', views.conversation_list, name='conversation_list'),
]