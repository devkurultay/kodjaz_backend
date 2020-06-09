from django.contrib.auth import logout

from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import RefreshTokenSerializer
 

class LogoutView(GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        logout(request)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.set_cookie('refresh_token', '')
        response.set_cookie('access_token', '')
        return response
