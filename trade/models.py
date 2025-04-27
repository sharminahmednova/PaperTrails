from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from adminhome.models import Book  

class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='trade_products/')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_tradeable(self):
        age = timezone.now() - self.created_at
        return age >= timedelta(days=30)


class TradeRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_trades')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_trades')
    offered_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='offered_in_trades')  # Remove null=True
    requested_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='requested_in_trades')
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')
    ], default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)