from django.shortcuts import render
from django.db.models import Max, Min
from django.template.loader import render_to_string
import json
from django.http import JsonResponse
# Create your views here.
def HomePage(request):

        
    return render(request, 'home.html', {})


