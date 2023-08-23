from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
import json 
from rest_framework.decorators import api_view
from user_details.models import UserDetails
from product_details.models import *
from transaction_details.models import Transaction
from transaction_details.serializers import TransactionSerializer
from cart_details.models import Cart
import stripe
from decimal import Decimal
import json


class ShipmentView(APIView):
    def post(self, request):
        data = request.data
        serializer = AddShipmentSerializer(data=data)
        if serializer.is_valid():
            address = request.data['address']
            city = request.data['city']
            state = request.data['state']
            zip = request.data['zip']
            user_id = request.data['user_id']
            firstname = request.data['firstname']
            lastname = request.data['lastname']
            user = UserDetails.objects.get(id=user_id)
            shipment = ShipmentDetails.objects.create(
                address = address,
                city = city,
                state = state,
                zip = zip,
                user_id = user,
                last_name=lastname,
                first_name=firstname
            )
            shipment.save()
            return Response({'data' : serializer.data, 'error' : False, 'msg' : "Success"}, status.HTTP_202_ACCEPTED)
        return Response({ 'error' : True, 'msg' : "Shipment Address cannot be added"}, status.HTTP_204_NO_CONTENT)
    def get(self, request):
        shipment = ShipmentDetails.objects.all()
        if shipment is not None:
            serializer = ShipmentSerializer(shipment, many=True)
            return Response({'data' : serializer.data, 'error' : False}, status.HTTP_202_ACCEPTED)
        return Response({'msg' : 'No data to show', 'error' : True}, status.HTTP_204_NO_CONTENT)
    
class ShowShipmentView(APIView):
    def get(self, request, id):
        user = UserDetails.objects.get(id=id)
        if user is not None:
            shipment = ShipmentDetails.objects.filter(user_id = user)
            if shipment is not None:
                serializer = ShipmentSerializer(shipment, many=True)
                return Response({'data' : serializer.data, 'error' : False}, status.HTTP_202_ACCEPTED)
        return Response({'msg' : 'No data to show', 'error' : True}, status.HTTP_204_NO_CONTENT)
    
class OrderView(APIView):

    def post(self, request):
        stripe.api_key = 'sk_test_51MpzUtLoFp1QEKARGxkOuCCDODAxX9TSy8VsNPZgN9bpFdragt0dy5yi2Lw7KXmxOoYUSXeRInCutS22rRnAMC99002om5S2rq'
        # print(request.data)
        serializer = AddOrderSerializer(data=request.data)
        # print(serializer)
    #     if serializer.is_valid():
    #         user_id = request.data['user_id']
    #         user_data = get_object_or_404(UserDetails, id=user_id)
    #         cart = Cart.objects.filter(user_data=user_data)
    #         total = Decimal('0')  # Initialize total as a Decimal
    #         discount = Decimal('0')  # Initialize discount as a Decimal
    #         if cart.exists():
    #             for product in cart:
    #                 price = product.product.disc_price
    #                 quantity = int(product.quantity)
    #                 total += (price * quantity)
    #                 discount += Decimal(product.product.p_price - price)  # Convert to Decimal
    #             shipping = Decimal('500')  # Initialize shipping as a Decimal
    #             total_bill = total + shipping
    #             order = Order.objects.create(user_id=user_data, total_bill=total_bill, discount=discount, bill_payed='0', payment_type='None', created_at=timezone.now(), updated_at=timezone.now())
    #             order_name = str(order.o_id)  # Convert order.o_id to string
    #             session = stripe.checkout.Session.create(
    #                 line_items=[{
    #                     'price_data': {
    #                         'currency': 'usd',
    #                         'product_data': {
    #                             'name': order_name,
    #                         },
    #                         'unit_amount': int(total_bill * 100),  # Convert to cents
    #                     },
    #                     'quantity': 1,
    #                 }],
    #                 mode='payment',
    #                 success_url='http://localhost:3000/product',
    #                 cancel_url='http://localhost:3000/checkout'
    #             )
    #             url = session.url
    #             session_id = session.id
    #             request.session['id'] = session_id
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            card_number = serializer.validated_data['card_number']
            exp_month = serializer.validated_data['exp_month']
            exp_year = serializer.validated_data['exp_year']
            cvc = serializer.validated_data['cvc']
            payment = request.data['payment_type']

            
            user_data = get_object_or_404(UserDetails, id=user_id)
            cart = Cart.objects.filter(user_data=user_data)
            total = Decimal('0')
            discount = Decimal('0')
            # print('Into ser')
            if cart.exists():
                # print('into if')
                for product in cart:
                    # print('into for')
                    price = product.product.disc_price
                    quantity = int(product.quantity)
                    total += (price * quantity)
                    discount += Decimal(product.product.p_price - price)
                
                shipping = Decimal('500')
                total_bill = total + shipping
                if payment == 'Stripe':
                    try:
                        payment_method = 'tok_visa'
                        payment_method = stripe.PaymentMethod.create(
                            type="card",
                            card={
                                "number": "4242424242424242",  # Use a test card number
                                "exp_month": 12,
                                "exp_year": 2023,
                                "cvc": "123",
                            },
                        )

                        order = Order.objects.create(
                            user_id=user_data,
                            total_bill=total_bill,
                            discount=discount,
                            bill_payed='0',
                            payment_type='None',
                            created_at=timezone.now(),
                            updated_at=timezone.now()
                        )
                        
                        # Continue with the payment process
                        payment_intent = stripe.PaymentIntent.create(
                            amount=int(total_bill),
                            currency="usd",
                            payment_method='pm_card_visa',
                            confirm=True,
                        )
                        
                        # Mark the order as paid
                        order.bill_payed = total_bill
                        order.payment_type = 'Stripe'
                        order.save()

                        # Return a success response to the user
                        return Response({
                            'data': serializer.data,
                            'error': False,
                            'msg': 'Order Created and Payment Successful',
                        }, status=status.HTTP_202_ACCEPTED)

                    except stripe.error.CardError as e:
                        return Response({
                            'error': True,
                            'msg': str(e.user_message)
                        }, status=status.HTTP_400_BAD_REQUEST)
                elif payment == 'Cash':
                    order = Order.objects.create(
                            user_id=user_data,
                            total_bill=total_bill,
                            discount=discount,
                            bill_payed='0',
                            payment_type='None',
                            created_at=timezone.now(),
                            updated_at=timezone.now()
                        )
                    order.save()
                    cart.delete()
                    # orderSerializer = ViewOrderSerializer(order)
                    return Response({
                            'data': serializer.data,
                            'error': False,
                            'msg': 'Order Created Successfully',
                        }, status=status.HTTP_202_ACCEPTED)
                return Response({
                'error': True,
                'msg': 'Cannot Create Order, Your cart is empty'
            }, status=status.HTTP_204_NO_CONTENT)
        return Response({
            'error': True,
            'msg': 'Cannot Create Order'
        }, status=status.HTTP_204_NO_CONTENT)
    

    def get(self, request):
        order = Order.objects.all()
        if order is not None:
            serializer = OrderSerializer(order, many=True)
            return Response({
                'data' : serializer.data,
                'error'  : False,
            })
        return Response({
            'error' : True,
            'msg' : 'There is an error Fetching data' 
        })
      
class UpdateOrderView(APIView):

    def post(self, request):
        serializer = UpdateOrderSerializer(data=request.data)
        if serializer.is_valid():
            user_data = request.data['user_id']
            order_id = request.data['order_id']
            payment = request.data['payment_type']
            order = Order.objects.get(o_id=order_id)
            cart = Cart.objects.filter(user_data=user_data)
            if payment == 'Stripe':
                id = request.session.get('id')
                order.payment_type = payment
                order.bill_payed = order.total_bill
                order.save()
                cart.delete()
                add = Transaction.objects.create(order=order, transaction_id = id, created_at=timezone.now(), updated_at=timezone.now())
                transaction_serializer = TransactionSerializer(add)
            elif payment == 'Cash':
                order.payment_type = payment
                order.bill_payed = 'pending' 
                order.save() 
                cart.delete()
            return Response({
                'data' : serializer.data,
                'error' : False,
                'msg' : 'Order Updated SuccessFully'
            }, status.HTTP_202_ACCEPTED)
        return Response({
            'error' : True,
            'msg' : 'Cannot Create Order, Your Order is not Found'
        }, status.HTTP_204_NO_CONTENT)
    
    def get(self, request,id):
        order = Order.objects.filter(user_id_id = id)
        if order is not None:
            serializer = OrderSerializer(order, many=True)
            return Response({
                'data' : serializer.data,
                'error'  : False,
            })
        return Response({
            'error' : True,
            'msg' : 'There is an error Fetching data' 
        })


class UpdateStatusView(APIView):

    def post(self, request):
        serializer = UpdateStatusSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            order_id = request.data['o_id']
            status = request.data['o_status']
            order = Order.objects.get(o_id=order_id)
            order.o_status = status
            order.save()
            return Response({
                'data' : serializer.data,
                'error' : False,
                'msg' : 'Order Status Updated SuccessFully'
            })
        return Response({
            'error' : True,
            'msg' : 'Cannot Update Order, Your Order is not Found'
        }, status.HTTP_204_NO_CONTENT) 

