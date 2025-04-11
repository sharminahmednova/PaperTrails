from django.db import models
from django import forms
# Create your models here.
class laptop(models.Model):
    password=models.CharField(max_length=50)
    re_pass=models.CharField(max_length=50)
    laptop=models.CharField(max_length=50)
    re_laptop=models.EmailField(max_length=50)
    email=models.EmailField(max_length=50)
    about=models.CharField(max_length=50)
    textarea=models.CharField(max_length=50)
    checkbox=models.CharField(max_length=50)
    ram=models.IntegerField()
    
   
