from rest_framework import serializers
from django.db import transaction
from djoser.serializers import UserSerializer
from .models import (Category, Subcategory, Product, ShoppingCart, GoodInCart)
from rest_framework.exceptions import ValidationError
from users.models import CustomUser


class CustomUserSerializer(UserSerializer):

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'name', 'surname',
                  )


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('name', 'slug', 'image')


class CategorySerializer(serializers.ModelSerializer):
    subs = SubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ('name', 'slug', 'image', 'subs')


class ProductSerializer(serializers.ModelSerializer):
    subcategory = serializers.StringRelatedField()
    category = serializers.SerializerMethodField()
    big_image = serializers.ImageField()
    middle_sized_image = serializers.ImageField()
    small_image = serializers.ImageField()

    class Meta:
        model = Product
        fields = ('name', 'slug', 'category', 'subcategory', 'price', 'big_image', 'middle_sized_image',
                  'small_image')

    def get_category(self, obj):
        return obj.subcategory.category.name


class ProductInCartSerializer(serializers.ModelSerializer):
    """Products list with details about a certain product"""
    product = serializers.SerializerMethodField()

    class Meta:
        model = GoodInCart
        fields = ('product', 'good_number', 'price')

    def get_product(self, obj):
        return ProductSerializer(
            Product.objects.filter(
                id=obj.product.id
            ), context=self.context, many=True
        ).data


class CartManipulateSerializer(serializers.ModelSerializer):
    """Manipulations with goods in a cart"""
    cart = serializers.PrimaryKeyRelatedField(
        queryset=ShoppingCart.objects.all(), required=False
    )

    class Meta:
        model = GoodInCart
        fields = ('cart', 'product', 'good_number', 'price')

    def validate(self, data):
        """checks if a product is not already in a cart"""
        if self.context.get('request').method == 'POST':
            if GoodInCart.objects.filter(product=data.get('product')).exists():
                raise ValidationError(
                    'This product is already in your cart, please change the quantity'
                )
        return data

    @transaction.atomic
    def create(self, validated_data):
        cart = ShoppingCart.objects.get(id=validated_data.get('cart_id'))
        product = validated_data.get('product')
        good_number = validated_data.get('good_number')
        price = product.price * good_number
        cart_item = GoodInCart.objects.create(
           cart=cart, product=product, good_number=good_number, price=price
        )
        return cart_item

    @transaction.atomic
    def update(self, instance, validated_data):
        good_number = validated_data.get('good_number')
        product = Product.objects.get(id=instance.product.id)
        instance.good_number = good_number + instance.good_number
        instance.price = product.price * instance.good_number
        if instance.good_number <= 0:
            instance.delete()
        else:
            instance.save()
        return instance


class CartSerializer(serializers.ModelSerializer):
    """Products list with details about all the products"""
    products = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCart
        fields = ('products', 'total_sum', 'total_goods_number')

    def get_products(self, obj):
        return ProductInCartSerializer(
            GoodInCart.objects.filter(cart=obj),
            context=self.context,
            many=True
        ).data

