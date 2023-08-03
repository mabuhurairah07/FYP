from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from user_details.models import UserDetails
from product_details.models import *
from transaction_details.models import Transaction
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
                order = Order.objects.create(user_id=user_data, total_bill=total , discount=discount, bill_payed = '0', payment_type='None',created_at = timezone.now(), updated_at = timezone.now())
                order.save()
                cart.delete()
                orderSerializer = ViewOrderSerializer(order)
                return Response({
                    'data' : orderSerializer.data,
                    'error' : False,
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
            payed = request.data['bill_payed']
            order = Order.objects.get(o_id=order_id)
            if order:
                order.payment_type = payment
                order.bill_payed = payed
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





            

        # user_id = request.data['user_id']
        # user = UserDetails.objects.get(id=user_id)
        # cart = Cart.objects.filter(user_data=user)
        # total = 0
        # discount = 0
        # if cart.exists():
        #     for items in cart:
        #         product_price = items.product.disc_price
        #         quantity = int(items.quantity)
        #         total += product_price * quantity
        #         discount += items.product.p_price - product_price
        # shipping = (total / 100) * 10

        # payment_type = request.data['payment_type']
        # total_bill = total + shipping
        # bill_payed = ''
            
