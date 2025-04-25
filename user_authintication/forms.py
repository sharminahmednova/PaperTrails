from django import forms
from user_authintication.models import Profile
from pages.models import Book, LendBorrow, BorrowRequest, DonateBook, DonateBookRequest

class RecentProduct(forms.Form):
    password=forms.CharField(widget=forms.PasswordInput)
    re_pass=forms.CharField(widget=forms.PasswordInput)
    laptop=forms.CharField()
    re_laptop=forms.CharField()
    email=forms.EmailField(initial='alif@gmail.com')
    about=forms.CharField(help_text='describe')
    textarea=forms.CharField(widget=forms.Textarea(attrs={'rows':4,'cols':40}))
    checkbox=forms.CharField(widget=forms.CheckboxInput)
    ram=forms.IntegerField(min_value=4,max_value=12)
    
    

    
class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = '__all__'

        
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"


class LendBorrowForm(forms.ModelForm):
    class Meta:
        model = LendBorrow
        fields = "__all__"


class BorrowRequestForm(forms.ModelForm):
    class Meta:
        model = BorrowRequest
        fields = "__all__"

class DonateBookForm(forms.ModelForm):
    class Meta:
        model = DonateBook
        fields = "__all__"

class DonateBookRequestForm(forms.ModelForm):
    class Meta:
        model = DonateBookRequest
        fields = "__all__"

        