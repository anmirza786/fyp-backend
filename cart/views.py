# from django.shortcuts import get_object_or_404
# from rest_framework.generics import (
#     ListCreateAPIView,
#     ListAPIView,
#     RetrieveUpdateDestroyAPIView,
# )
# from .serializers import OrderItemSerializer, OrderItemUpdateSerializer
# from rest_framework import permissions, status
# from rest_framework.response import Response
# from rest_framework.exceptions import NotAcceptable, ValidationError, PermissionDenied
# from django.utils.translation import ugettext_lazy as _

# from .models import Order, OrderItem
# from products.models import Product
# from notifications.utils import push_notifications


# class OrderItemAPIView(ListCreateAPIView):
#     serializer_class = OrderItemSerializer

#     def get_queryset(self):
#         user = self.request.user
#         queryset = OrderItem.objects.filter(Order__user=user)
#         return queryset

#     def create(self, request, *args, **kwargs):
#         user = request.user
#         Order = get_object_or_404(Order, user=user)
#         product = get_object_or_404(Product, pk=request.data["product"])
#         current_item = OrderItem.objects.filter(Order=Order, product=product)

#         if user == product.user:
#             raise PermissionDenied("This Is Your Product")

#         if current_item.count() > 0:
#             raise NotAcceptable("You already have this item in your shopping Order")

#         try:
#             quantity = int(request.data["quantity"])
#         except Exception as e:
#             raise ValidationError("Please Enter Your Quantity")

#         if quantity > product.quantity:
#             raise NotAcceptable("You order quantity more than the seller have")

#         Order_item = OrderItem(Order=Order, product=product, quantity=quantity)
#         Order_item.save()
#         serializer = OrderItemSerializer(Order_item)
#         total = float(product.price) * float(quantity)
#         Order.total = total
#         Order.save()
#         push_notifications(
#             Order.user,
#             "New Order product",
#             "you added a product to your Order " + product.title,
#         )

#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# class OrderItemView(RetrieveUpdateDestroyAPIView):
#     serializer_class = OrderItemSerializer
#     # method_serializer_classes = {
#     #     ('PUT',): OrderItemUpdateSerializer
#     # }
#     queryset = OrderItem.objects.all()

#     def retrieve(self, request, *args, **kwargs):
#         Order_item = self.get_object()
#         if Order_item.Order.user != request.user:
#             raise PermissionDenied("Sorry this Order not belong to you")
#         serializer = self.get_serializer(Order_item)
#         return Response(serializer.data)

#     def update(self, request, *args, **kwargs):
#         Order_item = self.get_object()
#         print(request.data)
#         product = get_object_or_404(Product, pk=request.data["product"])

#         if Order_item.Order.user != request.user:
#             raise PermissionDenied("Sorry this Order not belong to you")

#         try:
#             quantity = int(request.data["quantity"])
#         except Exception as e:
#             raise ValidationError("Please, input vaild quantity")

#         if quantity > product.quantity:
#             raise NotAcceptable("Your order quantity more than the seller have")

#         serializer = OrderItemUpdateSerializer(Order_item, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def destroy(self, request, *args, **kwargs):
#         Order_item = self.get_object()
#         if Order_item.Order.user != request.user:
#             raise PermissionDenied("Sorry this Order not belong to you")
#         Order_item.delete()
#         push_notifications(
#             Order_item.Order.user,
#             "deleted Order product",
#             "you have been deleted this product: "
#             + Order_item.product.title
#             + " from your Order",
#         )

#         return Response(
#             {"detail": _("your item has been deleted.")},
#             status=status.HTTP_204_NO_CONTENT,
#         )