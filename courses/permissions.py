from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS