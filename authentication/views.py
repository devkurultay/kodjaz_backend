from django.contrib.auth import login
from django.contrib.auth import logout
from django.middleware.csrf import get_token

from rest_framework import permissions
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import RefreshTokenSerializer
from .serializers import UserCreateSerializer


class LoginView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        # Perform session based login
        login(request, serializer.user)
        
        response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        # Set csrf cookie
        response['X-CSRFToken'] = get_token(request)
        return response


class LogoutView(GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        logout(request)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.set_cookie('refresh_token', '')
        response.set_cookie('access_token', '')
        response.set_cookie('X-CSRFToken', '')
        return response


class CreateUserAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserCreateSerializer
