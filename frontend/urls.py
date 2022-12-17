from django.urls import path
from django.urls import re_path

from .views import index

app_name = 'frontend'

urlpatterns = [
    path('', index),  # for the empty url
    re_path(r'^.*/$', index)  # for all other urls
]
