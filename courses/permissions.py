from rest_framework.permissions import IsAdminUser


class IsAdminMixin():
    permission_classes = [IsAdminUser]
