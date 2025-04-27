from django.urls import path
from . import views

urlpatterns = [
    path('login', views.LoginPage, name='login'),
    path('register', views.RegisterPage, name='register'),
    path('logout', views.Logout, name='logout'),
    path('profile', views.ProfilePage, name='profile'),
    path('activate/<str:uidb64>/<str:token>', views.VerifyEmailActivateAccount, name='activate'),
    path('reset-password/', views.ResetPassword1, name='resetPassword'),
    path('reset-password2/<str:uidb64>/<str:token>', views.ResetPassword2, name='resetPassword2'),
    
    
    path("recent/",views.details),  
    path('successfully/',views.send)
]