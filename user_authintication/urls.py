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

    path('dashboard/', views.DashboardPage, name='dashboard'),
    path('personalBook/', views.PersonalBookPage, name='personalBook'),
    path('addPersonalBook/', views.AddPersonalBookPage, name='addPersonalBook'),
    path('editPersonalBook/<str:id>', views.EditPersonalBookPage, name='editPersonalBook'),

    path('lendBorrowForm/', views.LendBookFormPage, name='lendBorrowForm'),
    path('borrowInside/<str:id>', views.BorrowInsidePage, name='borrowInside'),
    path('manageBorrowRequests/', views.ManageBorrowRequest, name='manageBorrowRequests'),
    path('manageBorrowRequestsInside/<str:id>', views.ManageBorrowRequestInside, name='manageBorrowRequestsInside'),
    path('manageBorrowedBooks/', views.ManageBorrowedBooks, name='manageBorrowedBooks'),
    path('donateBook/', views.DonateBookFormPage, name='donateBook'),
    path('donateBookRequest/<str:id>', views.DonationInsidePage, name='donateBookRequest'),
    path('manageDonateRequests/', views.ManageDonateRequest, name='manageDonateRequests'),
    path('manageDonateRequestsInside/<str:id>', views.ManageDonateRequestInside, name='manageDonateRequestsInside'),
    path('deleteBook/<str:id>', views.DeleteBook, name='deleteBook'),

    path("recent/",views.details),  
    path('successfully/',views.send)
]