from pyexpat import model
from rest_framework import serializers

from .models import GiftShop


class GiftShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = GiftShop
        fields = '__all__'
