from django.urls import path
from . import views
urlpatterns = [
    path('re/',views.django,name='paymentbybk'),
    path("pays/",views.payment_method),
]