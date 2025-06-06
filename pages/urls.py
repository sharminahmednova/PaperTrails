from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage, name='home'),
    path('bookListing/', views.BookListingPage, name='bookListing'),
    path('bookDetails/<str:id>', views.BookDetailsPage, name='bookDetail'),
    # path('bookListingfilter/', views.BookListingPageFilter, name='bookListingFilter'),
    path('lendBooks/', views.LendBookPage, name='lendBooks'),
    path('donateBooks/', views.DonateBookListPage, name='donateBooks'),
    path('toggle-wishlist/<int:book_id>/', views.ToggleWishlist, name='toggle_wishlist'),
    path('bookListingfilter/', views.BookListingPageFilter, name='bookListingFilter'),
    path('wishlist/', views.WishlistPage, name='wishlist'),
]