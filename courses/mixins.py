from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from courses.permissions import ReadOnly


class ReadOnlyOrAdminModelViewSetMixin(ModelViewSet):
    permission_classes = [ReadOnly|IsAdminUser]