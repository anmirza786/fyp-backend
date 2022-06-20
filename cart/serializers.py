from dataclasses import field, fields
from pyexpat import model
from rest_framework import serializers

from competitions.serializers import CompetitionSerializers, CompetitionTicketSerializers
from .models import *


class CartItemSerializer(serializers.ModelSerializer):

    # print(ticket_item)
    class Meta:
        model = CartItem
        # fields = ['is_ticket', 'ticket_item', 'id', 'gift']
        exclude = ['cart']


class CartItemRunSerializer(serializers.ModelSerializer):
    ticket = CompetitionTicketSerializers(read_only=True)
    # competiton = CompetitionSerializers
    # print(ticket_item)
    class Meta:
        model = CartItem
        # fields = ['is_ticket', 'ticket_item', 'id', 'gift']
        exclude = ['cart']


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemRunSerializer(read_only=True, many=True)

    # ticket = CompetitionTicketSerializers(read_only=True, many=True)
    class Meta:
        model = Cart
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderItemFetchSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'
