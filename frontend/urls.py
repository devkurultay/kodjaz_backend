from django.urls import path
from django.conf.urls import url

from .views import index

app_name = 'frontend'

urlpatterns = [
    path('', index),  # for the empty url
    url(r'^.*/$', index)  # for all other urls
]
