from django.db import models
from ckeditor.fields import RichTextField
from user_authintication.models import Profile

# Create your models here.

condition_choices = (
    ('New', "New"),
    ('Used', 'Used'),
    ('Better', "Used but like new")
)

class Book(models.Model):
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
    allow_bidding = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id} - {self.name}'

class Wishlist(models.Model):
    user = models.ForeignKey(Profile, related_name='wishlist', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='wishlisted_by', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f'{self.user.name} wishlisted {self.book.name}'

class WishlistItem(models.Model):
    book_name = models.CharField(max_length=250)
    user_name = models.CharField(max_length=100)
    book_id = models.IntegerField()  # Store the book ID to link back to the book
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_name} wishlisted {self.book_name}'

class Bid(models.Model):
    book = models.ForeignKey(Book, related_name='bids', on_delete=models.CASCADE)
    bidder = models.ForeignKey(Profile, related_name='bids', on_delete=models.CASCADE)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=(('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')), default='Pending')

    def __str__(self):
        return f'{self.bidder.name} bid ${self.amount} on {self.book.name}'

class LendBorrow(models.Model):
    book = models.ForeignKey(Book, related_name='book', on_delete=models.CASCADE)
    lender = models.OneToOneField(Profile, related_name='lender', on_delete=models.CASCADE)
    borrower = models.OneToOneField(Profile, related_name='borrower', on_delete=models.CASCADE)

    @property
    def lendTitle(self):
        return f'{self.lender.name} lends {self.book.name} to {self.borrower.name}'

    def __str__(self):
        return f'{self.lender.name} lent {self.book.name} to {self.borrower.name}'