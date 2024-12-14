from rest_framework.permissions import BasePermission, SAFE_METHODS

""" 
this permission allows users(both authenticated or annoynomus) only 
for GET method and all access for ADMIN user
"""
class IsAdminOrReadOnly(BasePermission):
    message = 'You are not permitted to perform this action'
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
              return True
        return request.user and request.user.is_authenticated and request.user.is_staff
    

"""
and this permission gives object level access - authenticated user can 
only acces their own object and admin can access anyones
"""
class IsOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
     
    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True
          
        #   if request.method in SAFE_METHODS:
        return request.user.is_staff