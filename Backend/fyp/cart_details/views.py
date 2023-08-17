from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cart
from user_details.models import UserDetails
from product_details.models import Product
from .serializers import *

class AddToCartView(APIView):
    def post(self, request):
        serializer = AddtoCartSerializer(data=request.data)
        if serializer.is_valid():
            user_id = request.data['user_data']
            p_id = request.data['product']
            quantity = request.data['quantity']
            created_at = timezone.now()
            updated_at = timezone.now()
            if not UserDetails.objects.get(id = user_id):
                return Response({'error' : True, 'data' : serializer.data, 'msg' : 'Login to Your Account'}, status.HTTP_204_NO_CONTENT)
            existing_cart_items = Cart.objects.filter(user_data=user_id, product=p_id)
            if existing_cart_items.exists():
                return Response({'message': 'Product already in cart.', 'error' : True}, status=status.HTTP_400_BAD_REQUEST)
            user = UserDetails.objects.get(id=user_id)
            product = Product.objects.get(p_id=p_id)
            cart = Cart.objects.create(
                user_data = user,
                product = product,
                quantity = quantity,
                created_at = created_at,
                updated_at = updated_at
                )
            cart.save()
            return Response({'data': serializer.data,'error' : False, 'msg' : 'Product Added Successfully'},status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CartView(APIView):

    def get(self, request, id):
        user = UserDetails.objects.get(id=id)
        cart_instance = Cart.objects.filter(user_data=user)
        if cart_instance is not None:
            serializer = CartSerializer(cart_instance, many=True)
            return Response({'data' : serializer.data, 'error' : False}, status.HTTP_202_ACCEPTED)
        return Response({'error' : True, 'msg' : 'Cannot Display Products'}, status.HTTP_204_NO_CONTENT)
    
    def post(self, request):
        print(request.data)
        serializer = CartUpdateSerializer(data=request.data)
        if serializer.is_valid():
            print('into for loop')
            user_id = request.data['user_data']
            p_id = request.data['product']
            quantity = request.data['quantity']
            print(request.data)
            user = UserDetails.objects.get(id=user_id)
            product = Product.objects.get(p_id=p_id)
            try:
                cart = Cart.objects.get(user_data=user, product=product)
            except Cart.DoesNotExist:
                return Response({'error': True, 'msg': 'Cart item not found.'}, status=status.HTTP_404_NOT_FOUND)
            cart.quantity = quantity
            cart.updated_at = timezone.now()
            cart.save()
            return Response({'data': serializer.data,'error' : False, 'msg' : 'Product Updated Successfully'},status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        
class DeleteCartView(APIView):
        
    def post(self, request):
        serializer = DSerializer(data=request.data)
        if serializer.is_valid():
            product = Product.objects.get(p_id=request.data['product'])
            user = UserDetails.objects.get(id=request.data['user_data'])
            cart = Cart.objects.get(user_data=user,product=product)
            cart.delete()
            return Response({'error': False, 'msg': 'Cart item deleted successfully.'}, status=status.HTTP_200_OK)
        return Response({'error': True, 'msg': 'Cart item not found.'}, status=status.HTTP_404_NOT_FOUND)