from django.conf import settings
from django.shortcuts import render

def index(request):
    context = { 'is_dev': settings.DEBUG }
    return render(request, 'frontend/index.html', context)
