from rest_framework import serializers
from .models import Order, OrderItem
from competitions.models import CompetitionTicket


class OrderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompetitionTicket
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    # product = OrderProductSerializer(required=False)
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderItemMiniSerializer(serializers.ModelSerializer):
    product = OrderProductSerializer(required=False)

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderItemUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'