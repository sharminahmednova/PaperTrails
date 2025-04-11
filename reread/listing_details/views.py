from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def send(req):
    return render(req,'listing_detail/submit.html')
def building_form(request):
    if request.method == "POST":
        frm=UserCreationForm(request.POST)
        if frm.is_valid():
            frm.save()
            return HttpResponseRedirect('/auth/successfully')
    else:

        frm=UserCreationForm
    return render(request,'listing_detail/build.html',{'form' : frm})

