from django.urls import path
from . import views
urlpatterns = [
    path('ua/',views.authin,name="authintc"),
    path("recent/",views.details),
    path('successfully/',views.send)
]