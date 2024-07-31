from rest_framework import permissions

class IsAdminOrManager(permissions.BasePermission):
    """Single permision for Admin and Manager"""
    def has_permission(self, request, view):
        if request and request.user and request.user.is_authenticated :
            if request.user.role == 'admin':
                return True
            elif request.method == 'PUT' and request.user.role == 'manager':
                return True
        return False
    
    

