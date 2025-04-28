from django import forms
from .models import Query
from .models import Reply
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }
class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write a reply...',
                'rows': 2
            }),
        }
class PostForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['text', 'image']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'What do you want to ask?',
                'rows': 3
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            })
        }