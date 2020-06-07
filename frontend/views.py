from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test


def is_staff(user):
    return user.is_staff


@login_required
@user_passes_test(is_staff)
def index(request):
    context = { 'is_dev': settings.DEBUG }
    return render(request, 'frontend/index.html', context)
