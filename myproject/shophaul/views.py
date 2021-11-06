from django.shortcuts import render
from .models import Seller
# Create your views here.


def home(request):
    return render(request, 'shophaul/index.html')
