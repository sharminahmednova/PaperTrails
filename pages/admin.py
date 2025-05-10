from django.contrib import admin
from user_authintication.models import Profile
from pages.models import Book, LendBorrow, BorrowRequest, DonateBook, DonateBookRequest, Wishlist, Bid, WishlistItem

# Register your models here.
admin.site.register(Profile)
admin.site.register(Book)
admin.site.register(Wishlist)
admin.site.register(Bid)
admin.site.register(WishlistItem)


admin.site.register(LendBorrow)
admin.site.register(BorrowRequest)
admin.site.register(DonateBook)
admin.site.register(DonateBookRequest)