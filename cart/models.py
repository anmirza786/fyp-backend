from decimal import ROUND_DOWN, Decimal, Rounded
from tkinter.tix import Tree
from django.contrib.auth import get_user_model
from django.db import models

from competitions.models import CompetitionTicket

User = get_user_model()


class OrderStatusEnum(models.IntegerChoices):
    ACTIVE = 1, 'Active'
    CART = 2 , 'Cart'
    DELIVERED = 3 , 'Delivered'

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             related_name='orders')
    total = models.DecimalField(max_digits=8,
                                decimal_places=2,
                                null=True,
                                blank=True)
    status = models.SmallIntegerField(max_length=30,
                              choices=OrderStatusEnum.choices,
                              default=OrderStatusEnum.CART)
    order_at = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=21, default='')
    address = models.CharField(max_length=256, default='')
    town = models.CharField(max_length=56, default='')
    postalcode = models.CharField(max_length=11, default='')
    country = models.CharField(max_length=250, default='')
    discount = models.DecimalField(decimal_places=0, max_digits=3, default=0)
    include_gift = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def total_win_vat(self):
        return ((self.total * Decimal(0.21) + self.total).quantize(
            Decimal('.01'), rounding=ROUND_DOWN))


class OrderItem(models.Model):
    order = models.ForeignKey('cart.Order',
                              on_delete=models.CASCADE,
                              related_name='order_items')
    # ecard = models.ForeignKey('ecard.Ecard',on_delete=models.CASCADE,related_name='orderitems',null=True)
    is_ticket = models.BooleanField(default=True)
    ticket = models.ForeignKey('competitions.CompetitionTicket',
                               on_delete=models.SET_NULL,
                               null=True, blank=True)
    gift = models.ForeignKey('giftshop.GiftShop',
                               on_delete=models.SET_NULL,
                               null=True, blank=True)

    def __str__(self):
        return str(self.order)


# class CartStatusEnum(models.IntegerChoices):
#     ACTIVE = 1, 'Active'
#     PASSIVE = 2, 'Passive'


# class Cart(models.Model):
#     user = models.ForeignKey(User,
#                              on_delete=models.SET_NULL,
#                              null=True,
#                              blank=True)
#     status = models.CharField(max_length=30,
#                               choices=CartStatusEnum.choices,
#                               default=CartStatusEnum.ACTIVE)
#     item = models.ForeignKey(CompetitionTicket,
#                              on_delete=models.SET_NULL,
#                              null=True,
#                              blank=True)
#     quantity = models.IntegerField(null=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.user