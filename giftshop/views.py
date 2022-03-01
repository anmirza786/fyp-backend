from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from rest_framework import permissions
from rest_framework.generics import RetrieveAPIView, ListAPIView
from .serializers import GiftShopSerializer
from .models import GiftShop


class GiftShopApiView(ListAPIView):

    # def get(self, request, format=None):
    #     gift = GiftShop.objects.all()
    #     serializer = GiftShopSerializer(gift, many=True)
    #     return Response(serializer.data)
    permission_classes = (permissions.AllowAny, )
    serializer_class = GiftShopSerializer

    def get_queryset(self):
        return GiftShop.objects.all()


class GiftApiView(RetrieveAPIView):

    permission_classes = (permissions.AllowAny, )
    serializer_class = GiftShopSerializer

    def get_queryset(self):
        return GiftShop.objects.all()