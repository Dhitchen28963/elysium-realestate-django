from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def my_real_estate(request):
    return HttpResponse("Hello, Elysium!")