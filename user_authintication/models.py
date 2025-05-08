from django.db import models
from django import forms
from django.contrib.auth.models import User

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
    
   



class Profile(models.Model):

    profileUser = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)

    name = models.CharField(max_length=250)
    email = models.CharField(max_length=255)

    phone = models.CharField(max_length=15)

    address = models.TextField(null=True, blank=True)
    contact_details = models.TextField(null=True, blank=True)
    # username_optional= models.CharField(null=True,blank=True,max_length=255)

    profile_pic = models.ImageField(upload_to='media/profilePic', null=True, blank=True)


    def __str__(self):
        return f'{self.id}-{self.name}'
    
