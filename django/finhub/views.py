from django.shortcuts import render
from django.http import HttpResponse
import os


# Create your views here.
def finhub(request):
    return HttpResponse("Hello, world. You're at the finhub site.")