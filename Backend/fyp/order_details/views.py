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


class ShipmentView(APIView):
    def post(self, request):
        data = request.data
        print(data)
        serializer = AddShipmentSerializer(data=data)
        if serializer.is_valid():
            address = request.data['address']
            city = request.data['city']
            state = request.data['state']
            zip = request.data['zip']
            user_id = request.data['user_id']
            firstname = request.data['first_name']
            lastname = request.data['last_name']
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
        serializer = AddOrderSerializer(data=request.data)
        if serializer.is_valid():
            user_id = request.data['user_id']
            user_data  = get_object_or_404(UserDetails, id=user_id)
            cart = Cart.objects.filter(user_data=user_data)
            print(cart)
            total = 0
            discount = 0
            if cart.exists():
                for product in cart:
                    price = product.product.disc_price
                    quantity = int(product.quantity)
                    total  +=  (price * quantity)
                    discount += product.product.p_price - price
                shipping = 500
                total_bill = total + shipping
                order = Order.objects.create(user_id=user_data, total_bill=total_bill , discount=discount, bill_payed = '0', payment_type='None',created_at = timezone.now(), updated_at = timezone.now())
                order.save()
                bill = float(total_bill)
                cart.delete()
                orderSerializer = ViewOrderSerializer(order)
                session = stripe.checkout.Session.create(
                line_items = [{
                        'price_data' : {
                        'currency' : 'usd',
                        'product_data' : {
                        'name' : order.o_id
                        },
                        'unit_amount' : int(bill)
                        },  
                        'quantity' : 1,
                    }],
                    mode = 'payment',
                    success_url = 'http://localhost:3000/product',
                    cancel_url = 'http://localhost:3000/checkout'
                )
                url = session.url
                session_id = session.id
                request.session['id'] = session_id
                return Response({
                    'data' : orderSerializer.data,
                    'order_bill' : total,
                    'shipping_charges' : shipping,
                    'error' : False,
                    'url' : url,
                    'msg' : 'Order Created SuccessFully'
                }, status.HTTP_202_ACCEPTED)
            return Response({
                'error' : True,
                'msg' : 'Cannot Create Order, Your cart is empty'
            }, status.HTTP_204_NO_CONTENT)
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
            order_id = request.data['order_id']
            payment = request.data['payment_type']
            order = Order.objects.get(o_id=order_id)
            bill = float(order.total_bill)
            if payment == 'Stripe':
                id = request.session.get('id')
                order.payment_type = payment
                order.bill_payed = order.total_bill
                order.save()
                add = Transaction.objects.create(order=order, transaction_id = id, created_at=timezone.now(), updated_at=timezone.now())
                transaction_serializer = TransactionSerializer(add)
            elif payment == 'Cash':
                order.payment_type = payment
                order.bill_payed = 'pending' 
                order.save() 
            return Response({
                'data' : serializer.data,
                'error' : False,
                'msg' : 'Order Updated SuccessFully'
            }, status.HTTP_202_ACCEPTED)
        return Response({
            'error' : True,
            'msg' : 'Cannot Create Order, Your Order is not Found'
        }, status.HTTP_204_NO_CONTENT)  

