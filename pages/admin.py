from django.contrib import admin
from user_authintication.models import Profile
from pages.models import Book, Wishlist, Bid, WishlistItem

# Register your models here.
admin.site.register(Profile)
admin.site.register(Book)
admin.site.register(Wishlist)
admin.site.register(Bid)
admin.site.register(WishlistItem)

