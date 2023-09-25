from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import ShoppingCart


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.role == request.user.is_staff
                or request.user.is_superuser
            )

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            request.user.role == request.user.is_staff
            or request.user.is_superuser
        )


class IsCartOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        cart = ShoppingCart.objects.get(id=view.kwargs.get('shoppingcart_id'))
        return cart.customer == request.user

    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user