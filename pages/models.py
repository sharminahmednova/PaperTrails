from django.db import models
from ckeditor.fields import RichTextField
from user_authintication.models import Profile
from django.contrib.auth.models import User

# Create your models here.

condition_choices = (
    ('New', "New"),
    ('Used', 'Used'),
    ('Better', "Used but like new")
)

class Book(models.Model):

    owner = models.ForeignKey(User, related_name='owner', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=250)
    description = RichTextField()
    author = models.CharField(max_length=250, default='')
    genre = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    condition = models.CharField(max_length=50, choices=condition_choices, default='New')
    price = models.IntegerField()
    location = models.CharField(max_length=250)
    book_image = models.ImageField(upload_to='books/', null=True, blank=True)


    @property
    def is_free(self):
        return not self.book.exists() and not self.donateBook.exists()

    def __str__(self):
        return f'{self.id} - {self.name}'
    



class DonateBook(models.Model):
    book = models.ForeignKey(Book, related_name='donateBook', on_delete=models.CASCADE)
    owner = models.ForeignKey(Profile, related_name='donateOwner', on_delete=models.CASCADE)
    requestor = models.ForeignKey(Profile, related_name='donateRequestor', on_delete=models.CASCADE, null=True, blank=True)
    donate_date = models.DateTimeField(auto_now=True)
    donate_status = models.BooleanField(default=False)
    

    def __str__(self):
        return f'{self.owner.name} wants to donate {self.book.name}'
    

class DonateBookRequest(models.Model):
    donateBook = models.ForeignKey(DonateBook, related_name='donateBookRequest', on_delete=models.CASCADE)
    requestor = models.ForeignKey(Profile, related_name='requestor', on_delete=models.CASCADE)
    request_message = models.TextField(default='')
    request_date = models.DateTimeField(auto_now=True)
    request_status = models.BooleanField(default=False)

    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.requestor.name} wants to take {self.donateBook.book.name} as donation'
    

class LendBorrow(models.Model):
    book = models.ForeignKey(Book, related_name='book', on_delete=models.CASCADE)
    lender = models.ForeignKey(Profile, related_name='lender', on_delete=models.CASCADE)
    borrower = models.ForeignKey(Profile, related_name='borrower', on_delete=models.SET_NULL, null=True, blank=True)

    lend_date = models.DateTimeField(auto_now=True)

    lend_status = models.BooleanField(default=False)
    lend_duration = models.IntegerField(default=0)


    @property
    def lendTitle(self):
        return f'{self.lender.name} wants to lend {self.book.name} '

    def __str__(self):

        return f'{self.lender.name} wants to lend {self.book.name}'



class BorrowRequest(models.Model):

    lendBorrow = models.ForeignKey(LendBorrow, related_name='lendBorrow', on_delete=models.CASCADE)
    borrower = models.ForeignKey(Profile, related_name='requestedBorrower', on_delete=models.CASCADE)

    request_date = models.DateTimeField(auto_now=True)
    request_status = models.BooleanField(default=False)
    request_duration = models.IntegerField(default=0)

    request_message = models.TextField(null=True, blank=True)

    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    return_status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.borrower.name} wants to borrow {self.lendBorrow.book.name}'