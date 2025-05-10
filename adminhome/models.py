from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='book_images/')
    location = models.CharField(max_length=200, default='', blank=True)  # Added default value
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending'
    )
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    posted_at = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.title

class ReviewHistory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=[('approved', 'Approved'), ('rejected', 'Rejected')])
    timestamp = models.DateTimeField(auto_now_add=True)