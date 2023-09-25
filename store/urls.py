from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (CategoriesList, ProductViewSet, CartManipulateViewSet, CartViewSet)

router = DefaultRouter()

router.register(r'categories', CategoriesList)
router.register(r'products', ProductViewSet)
router.register(r'cart', CartViewSet)
router.register(
   r'cart/(?P<cart_id>\d+)/cart_edit',
   CartManipulateViewSet, basename='cart_edit'
)


urlpatterns = [
   path('', include(router.urls)),
]