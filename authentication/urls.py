from django.urls import path

from rest_framework_simplejwt import views as jwt_views

from authentication.views import LogoutView

app_name = 'authentication'

urlpatterns = [
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='api_logout'),
]
