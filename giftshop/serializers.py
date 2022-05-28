from dataclasses import fields
from pyexpat import model
from rest_framework import serializers

from .models import Ecard, GiftShop


class GiftShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = GiftShop
        fields = '__all__'


class EcardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ecard
        fields = '__all__'