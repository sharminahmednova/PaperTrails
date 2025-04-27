from django.contrib import admin
from .models import Product, TradeRequest  # or whatever your model names are

admin.site.register(Product)
admin.site.register(TradeRequest)
