from dataclasses import field, fields
from pyexpat import model
from rest_framework import serializers
from .models import *


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'is_ticket', 'ticket', 'gift']


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['id', 'is_ticket']


class OrderItemFetchSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'
