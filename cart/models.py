from decimal import ROUND_DOWN, Decimal, Rounded
from django.contrib.auth import get_user_model
from django.db import models


class OrderStatusEnum(models.IntegerChoices):
    ACTIVE = 1, 'Active'
    SOLD = 2, 'Sold'


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             related_name='orders')
    total = models.DecimalField(max_digits=8,
                                decimal_places=2,
                                null=True,
                                blank=True)
    status = models.CharField(max_length=30,
                              choices=OrderStatusEnum.choices,
                              default=OrderStatusEnum.ACTIVE)
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
    title = models.CharField(max_length=255, null=True)
    ticket = models.ForeignKey('competitions.CompetitionTicket',
                               on_delete=models.CASCADE,
                               null=True)
    ticket_name = models.CharField(max_length=4, null=True, default='')

    def __str__(self):
        return str(self.ticket_name)
