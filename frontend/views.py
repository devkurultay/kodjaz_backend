from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    context = { 'test': 'test' }
    return render(request, 'frontend/index.html', context)
