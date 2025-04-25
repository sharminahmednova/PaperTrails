from django.contrib import admin
from user_authintication.models import Profile 
from pages.models import Book, LendBorrow, BorrowRequest, DonateBook, DonateBookRequest
# Register your models here.


admin.site.register(Profile)
admin.site.register(Book)
admin.site.register(LendBorrow)
admin.site.register(BorrowRequest)
admin.site.register(DonateBook)
admin.site.register(DonateBookRequest)