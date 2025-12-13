from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée : 
    - Tout le monde peut LIRE (GET)
    - Seulement le propriétaire peut MODIFIER/SUPPRIMER (PUT/PATCH/DELETE)
    """
    
    def has_object_permission(self, request, view, obj):
        # Lecture autorisée pour tout le monde
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        
        # Modification/suppression seulement pour le propriétaire
        return obj.seller == request.user


class IsOwner(permissions.BasePermission):
    """
    Permission personnalisée : 
    Seulement le propriétaire peut accéder à l'objet
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.seller == request.user
