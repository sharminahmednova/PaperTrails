

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homeadmin'),
    path('approve/<int:book_id>/', views.approve_book, name='approve_book'),
    path('reject/<int:book_id>/', views.reject_book, name='reject_book'),
    path('history/', views.history, name='history'),
    path('profile/', views.AdminProfile, name='admin_profile'),
    path('get-books/', views.get_books, name='get_books'),

]
