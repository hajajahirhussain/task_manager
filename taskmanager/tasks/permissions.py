from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only admins to edit/delete all users tasks.
    Normal users can only view (GET).
    """

    def has_permission(self, request, view):
        # print(f"User: {request.user}, Is Admin: {request.user.is_staff}")  # Debugging

        # Allow GET requests for all users
        if request.method in permissions.SAFE_METHODS:
            return True  
        
        # Allow POST, PUT, DELETE only for admin users
        return request.user.is_authenticated and request.user.is_staff
    
class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission:
    - Admins can do everything.
    - Normal users can only manage their own tasks.
    - Everyone can view (GET).
    """

    def has_object_permission(self, request, view, obj):
        # Allow GET (read-only) requests for everyone
        if request.method in permissions.SAFE_METHODS:
            return True  

        # Allow full access to admins
        if request.user.is_staff:
            return True  

        # Allow users to edit/delete only their own tasks
        return obj.user == request.user
    