from django import forms
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
    
    

    
