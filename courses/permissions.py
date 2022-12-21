from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsSubmissionOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, submission_obj):
        return submission_obj.user.id == request.user.id
