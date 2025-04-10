
from django.shortcuts import render
from payments.models import pay_method
# Create your views here.
def django(req):
    return render(req,'payment/p.html')
def payment_method(request):
    pay_m = pay_method.objects.all()
    return render (request, 'payment/pay.html',{'pay' : pay_m})