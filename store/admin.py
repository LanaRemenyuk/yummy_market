from django.contrib import admin

from .models import (Category, Subcategory, Product, ShoppingCart, GoodInCart)

EMPTY_VALUE = 'no info here yet'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = EMPTY_VALUE


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = EMPTY_VALUE


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'subcategory', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = EMPTY_VALUE


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_sum', 'total_goods_number')
    empty_value_display = EMPTY_VALUE


@admin.register(GoodInCart)
class GoodInCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'good_number', 'price')
    empty_value_display = EMPTY_VALUE