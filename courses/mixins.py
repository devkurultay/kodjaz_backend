from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from courses.permissions import ReadOnly


class ReadOnlyOrAdminModelViewSetMixin(ModelViewSet):
    permission_classes = [ReadOnly|IsAdminUser]


class UserContextMixin:
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"user": self.request.user})
        return context
