from django.contrib import admin
from user_authintication.models import Profile 
from pages.models import Book
# Register your models here.


admin.site.register(Profile)
admin.site.register(Book)