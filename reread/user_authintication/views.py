from django.shortcuts import render
from user_authintication.forms import RecentProduct
from django.http import HttpResponseRedirect
from .models import laptop
# Create your views here.
def authin(req):
    return render(req,'user_auth/ua.html')
def send(req):
    return render(req,'user_auth/submit.html')
def details(request):
    if request.method == 'POST':
        frm= RecentProduct(request.POST)
        if frm.is_valid():
            print('Valid form')
            pas=frm.cleaned_data['password']
            rpas=frm.cleaned_data['re_pass']
            lap=frm.cleaned_data['laptop']
            rlap=frm.cleaned_data['re_laptop']
            eml=frm.cleaned_data['email']
            abt=frm.cleaned_data['about']
            txt=frm.cleaned_data['textarea']
            chk=frm.cleaned_data['checkbox']
            rm=frm.cleaned_data['ram']
            
            buy=laptop(password=pas,re_pass=rpas,laptop=lap,re_laptop=rlap,email=eml,about=abt,textarea=txt,checkbox=chk,ram=rm)
            buy.save()

            return HttpResponseRedirect('/auth/successfully')
        else:
            frm= RecentProduct(auto_id=True,label_suffix=' - ')
            print('GET Statement')
    frm = RecentProduct()
    return render(request, 'user_auth/recent.html',{'form' : frm})