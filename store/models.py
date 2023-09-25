from django.utils.datetime_safe import datetime
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='category name',
                            help_text='enter the category name',)
    slug = models.SlugField(unique=True,
                            db_index=True,
                            verbose_name='category slug',
                            help_text='the slug is here')
    image = models.ImageField(
        upload_to='images/categories/',
        verbose_name='category image',
        help_text='upload the category image'
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='subcategory name',
                            help_text='enter the subcategory name', )
    slug = models.SlugField(unique=True,
                            db_index=True,
                            verbose_name='subcategory slug',
                            help_text='the slug is here')
    image = models.ImageField(
        upload_to='images/subcategories/',
        verbose_name='subcategory image',
        help_text='upload the subcategory image'
    )
    category = models.ForeignKey(
        Category,
        related_name='subs',
        on_delete=models.CASCADE,
        verbose_name='category',
    )

    class Meta:
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='product name',
                            help_text='enter the product name', )
    slug = models.SlugField(unique=True,
                            db_index=True,
                            verbose_name='product slug',
                            help_text='the slug is here')
    subcategory = models.ForeignKey(
        Subcategory,
        related_name='prods',
        on_delete=models.CASCADE,
        verbose_name='subcategory',
    )
    price = models.DecimalField(null=True,
                                max_digits=5,
                                decimal_places=2,
                                verbose_name='product price',
                                help_text='enter the product price'
                                )
    big_image = models.ImageField(upload_to='images/products/',
                                  verbose_name='big product image',
                                  help_text='upload the product image'
                                  )
    middle_sized_image = models.ImageField(upload_to='images/products/',
                                           verbose_name='middle-sized product image',
                                           help_text='upload the product image'
                                           )
    small_image = models.ImageField(upload_to='images/products/',
                                    verbose_name='small product image',
                                    help_text='upload the product image'
                                    )

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    customer = models.ForeignKey(
        User, related_name='cart',
        on_delete=models.CASCADE,
        verbose_name='customer',
        help_text='customer name here'
    )
    total_goods_number = models.IntegerField(
        null=True,
        default=0,
        verbose_name='number of goods in a cart',
        help_text='number of goods in a cart here'
    )
    total_sum = models.DecimalField(
        null=True,
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name='total price of goods in a cart',
        help_text='total price of goods in a cart here'
    )

    def __str__(self):
        return f'Cart {self.id}'


class GoodInCart(models.Model):
    cart = models.ForeignKey(
        ShoppingCart,
        related_name='cart_goods',
        on_delete=models.CASCADE,
        verbose_name='cart with goods',
        help_text='cart with goods here'
    )
    product = models.ForeignKey(Product,
                                null=True,
                                on_delete=models.CASCADE,
                                verbose_name='product in a cart',
                                help_text='product in a cart here'
                                )
    good_number = models.IntegerField(null=True,
                                      verbose_name='number of a certain product',
                                      help_text='number of a certain product')
    price = models.DecimalField(
        null=True,
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name='product price in a cart',
        help_text='here product price in a cart'
    )
    class Meta:
        verbose_name = "Goods in cart"
        verbose_name_plural = "Goods in cart"


@receiver(post_save, sender=User)
def shopping_cart_create(sender, **kwargs):
    """Shopping cart gets created when authenticated"""
    user = kwargs['instance']
    cart = ShoppingCart.objects.create(customer=user)
    cart.save()


@receiver([post_save, post_delete], sender=GoodInCart)
def cart_manipulations(sender, **kwargs):
    """Updating the total cost and number of items in a cart after manipulations"""
    cart_item = kwargs['instance']
    cart = ShoppingCart.objects.get(id=cart_item.cart.id)
    result = GoodInCart.objects.filter(cart=cart).aggregate(
        total_sum=Sum('price'), total_goods_number=Sum('good_number'))
    cart.total_price = result['total_sum']
    cart.total_count = result['total_goods_number']
    if not result['total_goods_number'] and not result['total_sum']:
        cart.total_price = 0
        cart.total_count = 0
    cart.save()

