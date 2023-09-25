from .models import Category, Product, ShoppingCart, GoodInCart
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from users.models import CustomUser
from users.pagination import UsersPagination
from .serializers import (CustomUserSerializer, CategorySerializer,
                          ProductSerializer, CartSerializer, CartManipulateSerializer)
from .permissions import AdminPermission, IsCartOwner


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AdminPermission]
    pagination_class = UsersPagination


class CategoriesList(mixins.ListModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartManipulateViewSet(
    mixins.CreateModelMixin, mixins.UpdateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    serializer_class = CartManipulateSerializer
    #permission_classes = (IsCartOwner,)

    def get_queryset(self):
        cart = get_object_or_404(ShoppingCart, id=self.kwargs.get('cart_id'))
        queryset = cart.cart_goods.all()
        return queryset

    def perform_create(self, serializer):
        cart = get_object_or_404(GoodInCart, id=self.kwargs["cart_id"])
        serializer.save(
            cart=cart)

    def create(self, request, *args, **kwargs):
        request.data['cart'] = self.kwargs.get('cart_id')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if instance.id is None:
            return Response(status=status.HTTP_204_NO_CONTENT)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_queryset()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = ShoppingCart.objects.all()
    permission_classes = (IsCartOwner,)
    serializer_class = CartSerializer