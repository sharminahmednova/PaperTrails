from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage, name='home'),
    path('bookListing/', views.BookListingPage, name='bookListing'),
    path('bookDetails/<str:id>', views.BookDetailsPage, name='bookDetail'),
    path('bookListingfilter/', views.BookListingPageFilter, name='bookListingFilter'),
    path('wishlist/', views.WishlistPage, name='wishlist'),
    path('toggle-wishlist/<int:book_id>/', views.ToggleWishlist, name='toggle_wishlist'),
    path('submit-bid/<int:book_id>/', views.SubmitBid, name='submit_bid'),
]