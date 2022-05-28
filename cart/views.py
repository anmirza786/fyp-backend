from datetime import datetime, timedelta
from unicodedata import decimal
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from random import random
from cart.models import  Order, OrderItem, OrderStatusEnum
from cart.serializers import OrderItemFetchSerializer, OrderItemSerializer, OrderSerializer
from competitions.models import CompetitionTicket, CompetitionTicketStatusEnum
from giftshop.models import Ecard
from django.utils import timezone


class ActiveCartApiView(RetrieveAPIView):
    serializer_class = OrderSerializer

    def get_object(self):
        cart, _ = Order.objects.get_or_create(user=self.request.user,
                                             status=OrderStatusEnum.CART)
        return cart

class RetriveOrderitemsApiView(RetrieveAPIView):
    serializer_class = OrderItemFetchSerializer

    def get_queryset(self):
        if Order.objects.filter(id=self.kwargs['pk']).exists():
            return OrderItem.objects.filter(order_id=self.kwargs['pk'])
        return OrderItem.objects.none()

class CartItemCreateApiView(CreateAPIView):
    serializer_class = OrderItemSerializer

    def perform_create(self, serializer):
        order, _ = Order.objects.get_or_create(user=self.request.user,
                                             status=OrderStatusEnum.CART)
        serializer.validated_data['order'] = order

        if serializer.validated_data['is_ticket']:
            available_ecards = Ecard.objects.exclude(
                cartitems_cartuser_id=self.request.user.id)
            if not available_ecards:
                ecards = Ecard.objects.all()
                random_ecard = random.choice(ecards)
            else:
                random_ecard = random.choice(available_ecards)
            serializer.validated_data['ecard'] = random_ecard

        return super(CartItemCreateApiView,
                     self).perform_create(serializer=serializer)
# class 
# class OrderApiView(RetrieveAPIView):
#     serializer_class = OrderSerializer

#     def post(self, request, format=None):
#         try:
#             user = self.request.user
#             cartItems = Cart.objects.filter(
#                 user=user.id,
#                 status=CartStatusEnum.CART).first().items.all()
#             if not cartItems:
#                 return Response({
#                     'error':
#                     'Oops. Your cart is empty. Please fill your cart before checking out.'
#                 })
#             cart = Cart.objects.filter(user=user.id,
#                                        status=CartStatusEnum.ACTIVE).first()
#             total = sum([i.quantity * i.price for i in cartItems])
#             discount = get_first_refer_discount(request.user)
#             total = round(total - (total * decimal.Decimal(discount / 100)), 2)
#             data = self.request.data
#             order = Order.objects.create(user=self.request.user,
#                                          status=OrderStatusEnum.ACTIVE,
#                                          total=total,
#                                          discount=discount,
#                                          phone=data['phone'],
#                                          address=data['address'],
#                                          town=data['town'],
#                                          postcode=data['postcode'],
#                                          country=data['country'])
#             UserTransactions.objects.create(
#                 user=user,
#                 amount_paid=data['amount_paid'],
#                 date_time=data['date_time'],
#                 transaction_id=data['transaction_id'],
#                 payment_order_id=data['payment_order_id'],
#                 order=order)
#             user = request.user
#             set_affiliate_payment(user=user, amount=order.total, order=order)
#             include_gift = False
#             for item in cartItems:
#                 if item.is_ticket:
#                     ticket = item.ticket
#                     competition = ticket.competition
#                     competition.total_earned = competition.total_earned + item.price
#                     competition.save()
#                     ticket.status = CompetitionTicketStatusEnum.SOLD
#                     ticket.customer_id = user.id
#                     ticket.sold_time = datetime.now()
#                     ticket.save()
#                     OrderItem.objects.create(order=order,
#                                              title=item.title,
#                                              ticket=item.ticket,
#                                              ticket_name=item.ticket_name,
#                                              ecard=item.ecard,
#                                              price=item.price,
#                                              is_ticket=True)
#                 else:
#                     include_gift = True
#                     OrderItem.objects.create(order=order,
#                                              title=item.title,
#                                              gift=item.gift,
#                                              quantity=item.quantity,
#                                              price=item.price,
#                                              is_ticket=False)
#             order.include_gift = include_gift
#             order.save()
#             cart.status = CartStatusEnum.CLOSED
#             cart.save()
#             send_payment_email(user, order)
#             return Response({'success': 'order has been placed'})
#         except Exception as e:
#             raise e
#             return Response({'error': 'error while creating order'})


# class ReserveApiView(APIView):

#     def put(self, request, format=None):
#         try:
#             user = self.request.user
#             cartItems = Cart.objects.filter(
#                 user=user.id,
#                 status=CartStatusEnum.ACTIVE).first().items.all()
#             tickets = CompetitionTicket.objects.filter(customer=user)
#             if not cartItems:
#                 return Response({'error': 'Cart is empty'})
#             now = timezone.now()
#             for item in cartItems:
#                 if item.is_ticket:
#                     ticket = item.ticket

#                     if not (
#                             ticket.status
#                             == CompetitionTicketStatusEnum.RESERVED
#                             and item.ticket in tickets
#                     ) or ticket.status == CompetitionTicketStatusEnum.AVAILABALE:
#                         message = item.ticket_name
#                         item.delete()
#                         return Response({
#                             'error':
#                             'Oops. Ticket No: ' + message +
#                             ' purchased by someone else. \nKindly choose your ticket again!'
#                         })
#                     ticket.status = CompetitionTicketStatusEnum.RESERVED
#                     item.expiration_time = now + timedelta(minutes=10)
#                     item.save()
#                     ticket.save()
#             return Response({'success': 'Cart Reserved again.'})
#         except:
#             return Response({'error': 'error while Reserving'})