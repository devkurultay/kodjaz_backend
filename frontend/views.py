from django.conf import settings
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test

from rest_framework_simplejwt.tokens import RefreshToken

def is_staff(user):
    return user.is_staff


@login_required
@user_passes_test(is_staff)
def index(request):
    context = { 'is_dev': settings.DEBUG }
    content = loader.render_to_string('frontend/index.html', context, request)
    response = HttpResponse(content)
    # Set tokens (if the code executes here, then it's a is_staff user)
    value = request.COOKIES.get('refresh_token')
    if not value:
        user = request.user
        refresh = RefreshToken.for_user(user)
        response.set_cookie('refresh_token', str(refresh))
        response.set_cookie('access_token', str(refresh.access_token))
    return response
