from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    context = { 'is_dev': settings.DEBUG }
    return render(request, 'frontend/index.html', context)
