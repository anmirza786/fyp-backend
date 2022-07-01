from datetime import datetime, timedelta
from unicodedata import decimal
from requests import delete, request
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from random import random
from rest_framework import permissions
from cart.models import Cart, CartItem, CartStatusEnum, Order, OrderItem, OrderStatusEnum
from cart.serializers import CartItemSerializer, CartSerializer, OrderItemFetchSerializer, OrderItemSerializer, OrderSerializer
from competitions.models import CompetitionTicket, CompetitionTicketStatusEnum
from giftshop.models import Ecard
from django.utils import timezone

# class ActiveCartApiView(RetrieveAPIView):
#     serializer_class = OrderSerializer

#     def get_object(self):
#         cart, _ = Order.objects.get_or_create(user=self.request.user,
#                                               status=OrderStatusEnum.CART)
#         return cart

# class RetriveOrderitemsApiView(RetrieveAPIView):
#     serializer_class = OrderItemFetchSerializer

#     def get_queryset(self):
#         if Order.objects.filter(id=self.kwargs['pk']).exists():
#             return OrderItem.objects.filter(order_id=self.kwargs['pk'])
#         return OrderItem.objects.none()

# class DeleteOrderitemsApiView(RetrieveAPIView):
#     serializer_class = OrderItemFetchSerializer

#     def get_queryset(self):
#         if Order.objects.filter(id=self.kwargs['pk']).exists():
#             return OrderItem.objects.filter(
#                 order_id=self.kwargs['pk']).delete()
#         return OrderItem.objects.none()

# class OrderItemCreateApiView(CreateAPIView):
#     serializer_class = OrderItemSerializer

#     def perform_create(self, serializer):
#         order, _ = Order.objects.get_or_create(user=self.request.user,
#                                                status=OrderStatusEnum.CART)
#         serializer.validated_data['order'] = order

#         if serializer.validated_data['is_ticket']:
#             available_ecards = Ecard.objects.exclude(
#                 cartitems_cartuser_id=self.request.user.id)
#             if not available_ecards:
#                 ecards = Ecard.objects.all()
#                 random_ecard = random.choice(ecards)
#             else:
#                 random_ecard = random.choice(available_ecards)
#             serializer.validated_data['ecard'] = random_ecard

#         return super(OrderItemCreateApiView,
#                      self).perform_create(serializer=serializer)


class ActiveCartApiView(RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = (permissions.AllowAny, )

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(status=CartStatusEnum.ACTIVE)
        #  user=self.request.user)

        return cart


class CartItemCreateApiView(CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = (permissions.AllowAny, )
    print("@@")

    def perform_create(self, serializer):
        print("a")
        cart, _ = Cart.objects.get_or_create(user=self.request.user,
                                             status=CartStatusEnum.ACTIVE)
        # print(cart)
        serializer.validated_data['cart'] = cart
        serializer.validated_data['is_ticket']
        ticket = serializer.validated_data['ticket']

        ticket = CompetitionTicket.objects.get(id=ticket.id)

        if ticket.status == CompetitionTicketStatusEnum.AVAILABLE:
            # ticket.customer_id = self.request.user.id
            # ticket.sold_time = datetime.now()
            ticket.status = CompetitionTicketStatusEnum.RESERVED
            ticket.save()
            print('a')
        else:
            print('aa')
            return Response("Already Added")
        return super(CartItemCreateApiView,
                     self).perform_create(serializer=serializer)


class CartItemDeleteApiView(APIView):

    def delete(self, request, pk, format=None):
        cartitem = CartItem.objects.get(pk=pk)

        # print(cartitem.ticket.id)
        ticket = CompetitionTicket.objects.get(id=cartitem.ticket.id)

        if ticket.status == CompetitionTicketStatusEnum.RESERVED:
            # ticket.customer_id = self.request.user.id
            # ticket.sold_time = datetime.now()
            ticket.status = CompetitionTicketStatusEnum.AVAILABLE
            ticket.save()

        else:

            return Response("Already Deleted")
        cartitem.delete()
        return Response('Deleted Successfully')


class OrderApiView(RetrieveAPIView):
    serializer_class = OrderSerializer

    def post(self, request, format=None):
        try:
            user = self.request.user
            cartItems = Cart.objects.filter(
                user=user.id,
                status=CartStatusEnum.ACTIVE).first().cart_items.all()
            if not cartItems:
                return Response({
                    'error':
                    'Oops. Your cart is empty. Please fill your cart before checking out.'
                })
            cart = Cart.objects.filter(user=user.id,
                                       status=CartStatusEnum.ACTIVE).first()
            total = sum([i.price for i in cartItems])
            # discount = get_first_refer_discount(request.user)
            total = round(total, 2)
            data = self.request.data
            order = Order.objects.create(user=self.request.user,
                                         status=OrderStatusEnum.ACTIVE,
                                         total=total,
                                        #  discount=discount,
                                        #  phone=data['phone'],
                                        #  address=data['address'],
                                        #  town=data['town'],
                                        #  postcode=data['postcode'],
                                        #  country=data['country']
                                        )
            # UserTransactions.objects.create(
            #     user=user,
            #     amount_paid=data['amount_paid'],
            #     date_time=data['date_time'],
            #     transaction_id=data['transaction_id'],
            #     payment_order_id=data['payment_order_id'],
            #     order=order)
            user = request.user
            # set_affiliate_payment(user=user, amount=order.total, order=order)
            include_gift = False
            for item in cartItems:
                if item.is_ticket:
                    ticket = item.ticket
                    competition = ticket.competition
                    competition.total_earned = competition.total_earned + item.price
                    competition.save()
                    ticket.status = CompetitionTicketStatusEnum.SOLD
                    ticket.customer_id = user.id
                    ticket.sold_time = datetime.now()
                    ticket.save()
                    OrderItem.objects.create(order=order,
                                            #  title=item.title,
                                             ticket=item.ticket,
                                            #  ticket_name=item.ticket_name,
                                            #  ecard=item.ecard,
                                             price=item.price,
                                             is_ticket=True)
                else:
                    include_gift = True
                    OrderItem.objects.create(
                        order=order,
                        # title=item.title,
                        gift=item.gift,
                        #  quantity=item.quantity,
                        price=item.price,
                        is_ticket=False)
            order.include_gift = include_gift
            order.save()
            cart.status = CartStatusEnum.CLOSED
            cart.save()
            # send_payment_email(user, order)
            return Response({'success': 'order has been placed'})
        except Exception as e:
            raise e
            return Response({'error': 'error while creating order'})


class ReserveApiView(APIView):

    def put(self, request, format=None):
        try:
            user = self.request.user
            cartItems = Cart.objects.filter(
                user=user.id,
                status=CartStatusEnum.ACTIVE).first().items.all()
            tickets = CompetitionTicket.objects.filter(customer=user)
            if not cartItems:
                return Response({'error': 'Cart is empty'})
            now = timezone.now()
            for item in cartItems:
                if item.is_ticket:
                    ticket = item.ticket

                    if not (
                            ticket.status
                            == CompetitionTicketStatusEnum.RESERVED
                            and item.ticket in tickets
                    ) or ticket.status == CompetitionTicketStatusEnum.AVAILABALE:
                        message = item.ticket_name
                        item.delete()
                        return Response({
                            'error':
                            'Oops. Ticket No: ' + message +
                            ' purchased by someone else. \nKindly choose your ticket again!'
                        })
                    ticket.status = CompetitionTicketStatusEnum.RESERVED
                    item.expiration_time = now + timedelta(minutes=10)
                    item.save()
                    ticket.save()
            return Response({'success': 'Cart Reserved again.'})
        except:
            return Response({'error': 'error while Reserving'})