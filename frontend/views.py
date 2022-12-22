import json
from django.conf import settings
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from rest_framework_simplejwt.tokens import RefreshToken
from .utils import static_fallback_open


def is_staff(user):
    return user.is_staff


@login_required
@user_passes_test(is_staff)
def index(request):
    """
    Example contents of asset-manifest.json
    {
        "files": {
            "main.css": "/static/css/main.d6678dc7.css",
            "main.js": "/static/js/main.d996b665.js",
            "index.html": "/index.html",
            "main.d6678dc7.css.map": "/static/css/main.d6678dc7.css.map",
            "main.d996b665.js.map": "/static/js/main.d996b665.js.map"
        },
        "entrypoints": [
            "static/css/main.d6678dc7.css",
            "static/js/main.d996b665.js"
        ]
    }
    """
    asset_manifest = {}
    with static_fallback_open("asset-manifest.json") as json_file:
        asset_manifest = json.load(json_file)
    react_css_bundle = asset_manifest["files"]["main.css"]
    react_js_bundle = asset_manifest["files"]["main.js"]

    context = {
        'is_dev': settings.DEBUG,
        "react_css_bundle": react_css_bundle,
        "react_js_bundle": react_js_bundle
    }
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
