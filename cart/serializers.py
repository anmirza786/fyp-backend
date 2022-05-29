from dataclasses import field, fields
from pyexpat import model
from rest_framework import serializers
from .models import *


class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        exclude = ['cart']


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(read_only=True, many=True)

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
