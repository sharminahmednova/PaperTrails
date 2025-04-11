from django.urls import path
from . import views
urlpatterns = [
    
    path('build/',views.building_form),
    path('successfully/',views.send)
]