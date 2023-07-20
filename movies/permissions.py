from rest_framework import permissions


class IsAuthenticatedOrIsEmployee(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
          request.user.is_authenticated
          and request.user.is_employee
        )
