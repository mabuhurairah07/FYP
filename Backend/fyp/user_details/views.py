from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import UserDetails
from order_details.models import *
from django.utils import timezone
import random
import string
from django.core.mail import send_mail
from datetime import datetime
# Create your views here.

from .serializers import *
class SignupView(APIView):

    def post(self, request):
        data = request.data
        serializer = SignupSerializer(data=data)
        if serializer.is_valid():
            user = UserDetails.objects.create(
                username = request.data['username'],
                email = request.data['email'],
                phone_no = request.data['phone_no'],
                created_at = timezone.now(),
                updated_at = timezone.now()
            )
            user.set_password(request.data['password'])
            user.save()
            return Response({'data': serializer.data,'error' : False, 'msg' : 'Account Created Successfully'},status.HTTP_201_CREATED)
        else:
           return Response(serializer.errors, status.HTTP_400_BAD_REQUEST, {'error' : True, 'msg' : 'Error Creating Account'})
        
class LoginView(APIView):

    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data = data)
        if serializer.is_valid():
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            if user is None:
                return Response({'data' : serializer.errors, 'error' : True, 'msg' : 'Cannot Login, User or Password Incorrect'},status.HTTP_400_BAD_REQUEST)
            else:
                user_data_fetch = UserDetails.objects.get(username=username)
                # serializer_data = UserSerializer(user_data_fetch)
                response_data = {
                    'id' : user_data_fetch.id,
                    'username' : user_data_fetch.username,
                }
                return Response({ 'data' : response_data , 'error' : False, 'msg' : 'Logged In Successfully'},status.HTTP_201_CREATED)

class SellerSignupView(APIView):

    def post(self, request):
        data = request.data
        serializer = SellerSignupSerializer(data=data)
        if serializer.is_valid():
            user = UserDetails.objects.create(
                username = request.data['username'],
                email = request.data['email'],
                phone_no = request.data['phone_no'],
                created_at = timezone.now(),
                updated_at = timezone.now(),
                is_seller = True   
            )
            user.set_password(request.data['password'])
            user.save()
            return Response({'data': serializer.data,'error' : False, 'msg' : 'Seller Account Created Successfully'},status.HTTP_201_CREATED)
        else:
           return Response(serializer.errors, status.HTTP_400_BAD_REQUEST, {'error' : True, 'msg' : 'Error Creating Seller Account'})
        
class SellerLoginView(APIView):

    def post(self, request):
        data = request.data
        serializer = SellerLoginSerializer(data = data)
        if serializer.is_valid():
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            seller = True
            if user is None:
                return Response({'data' : serializer.errors, 'error' : True, 'msg' : 'Cannot Login, Username or Password Incorrect'},status.HTTP_400_BAD_REQUEST)
            elif user is not None:
                user_data_fetch = UserDetails.objects.get(username=username, is_seller=seller)
                if user_data_fetch is None:
                   return Response({'data' : serializer.errors, 'error' : True, 'msg' : 'Cannot Login, Username or Password Incorrect'},status.HTTP_400_BAD_REQUEST) 
                else :
                    response_data = {
                        'id' : user_data_fetch.id,
                        'username' : user_data_fetch.username,
                    }
                return Response({'data' : response_data, 'error' : False, 'msg' : 'Seller Logged In Successfully'},status.HTTP_201_CREATED) 
                

class AdminSignupView(APIView):

    def post(self, request):
        data = request.data
        serializer = AdminSignupSerializer(data=data)
        if serializer.is_valid():
            user = UserDetails.objects.create(
                username = request.data['username'],
                email = request.data['email'],
                phone_no = request.data['phone_no'],
                created_at = timezone.now(),
                updated_at = timezone.now(),
                is_seller = True,
                is_admin = True   
            )
            user.set_password(request.data['password'])
            user.save()
            return Response({'data': serializer.data,'error' : False, 'msg' : 'Admin Account Created Successfully'},status.HTTP_201_CREATED)
        else:
           return Response(serializer.data, status.HTTP_400_BAD_REQUEST, {'error' : True, 'msg' : 'Error Creating Admin Account'})
        
class AdminLoginView(APIView):

    def post(self, request):
        data = request.data
        print(data)
        serializer = AdminLoginSerializer(data = data)
        if serializer.is_valid():
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            if user is None:
                return Response({'data' : serializer.errors, 'error' : True, 'msg' : 'Cannot Login, Username or Password Incorrect'},status.HTTP_400_BAD_REQUEST)
            elif user is not None:
                user_data_fetch = UserDetails.objects.get(username=username)
                if user_data_fetch is None:
                   return Response({'data' : serializer.errors, 'error' : True, 'msg' : 'Cannot Login, Username or Password Incorrect'},status.HTTP_400_BAD_REQUEST) 
                else :
                    response_data = {
                        'id' : user_data_fetch.id,
                        'username' : user_data_fetch.username,
                    }
                return Response({'data' : response_data, 'error' : False, 'msg' : 'Admin Logged In Successfully'},status.HTTP_201_CREATED) 
            
class AdminDetailsView(APIView):
    def get(self, request, id):
        admin = UserDetails.objects.filter(id=id, is_admin=True)
        if admin is not None:
            serializer = AdminDetailsSerializer(admin, many=True)
            return Response({
                'data' : serializer.data,
                'error' : False
            })
        return Response({
            'data' : serializer.errors,
            'error' : True
        })
    
    def post(self,request, id):
        admin = UserDetails.objects.get(id=id, is_admin=True)
        created_at = admin.created_at
        if admin is not None:
            name = request.data['username']
            phone_no = request.data['phone_no']
            email = request.data['email']
            admin.username = name
            admin.phone_no = phone_no
            admin.email = email
            admin.updated_at = timezone.now()
            admin.created_at = created_at
            admin.save()
            serializer = AdminDetailsSerializer(admin)
            return Response({
                'data' : serializer.data,
                'error' : False
            })
        return Response({
            'data' : serializer.errors,
            'error' : True
        })



class TotalUsersView(APIView):
    def get(self, request):
        allseller = self.get_allseller()
        allcustomers = self.get_allcustomers()
        if allseller is not None or allcustomers is not None:
            return Response({
                'allseller' : allseller,
                'allcustomers' : allcustomers,
                'error'  : False,
            })
        return Response({
            'error' : True,
            'msg' : 'There is an error Fetching data'
        })

    def get_allseller(self):
        seller = UserDetails.objects.filter(is_seller=True)
        if seller is not None:
            serializer = UserSerializer(seller, many=True)
            return serializer.data
        return []
  
    def get_allcustomers(self):
        customers = UserDetails.objects.filter(is_seller=False,is_admin=False)
        customers_count = UserDetails.objects.filter(is_seller=False,is_admin=False).count()
        if customers is not None:
            serializer = UserSerializer(customers, many=True)
            return {
                'data' : serializer.data,
                'count' : customers_count
            }
        return []


class DashboardView(APIView):
    def get(self, request, id):
            current_month = timezone.now().month
            current_year = timezone.now().year
            current_date = timezone.now().date()
            user = UserDetails.objects.get(id=id, is_admin=True)
            if user is None:
                return Response({
                'error' : True,
                'data' : 'User Not Found'
            })
            else:
                order = Order.objects.all()
                todayOrders = Order.objects.filter(updated_at__date=current_date)
                monthOrder = Order.objects.filter(updated_at__month=current_month, updated_at__year=current_year)
                monthCustomers = UserDetails.objects.filter(is_admin=False, is_seller=False, is_active=True, updated_at__month=current_month, updated_at__year=current_year)
                todayCustomers = UserDetails.objects.filter(is_admin=False, is_seller=False, is_active=True, updated_at__date=current_date)
                customer = UserDetails.objects.filter(is_admin=False, is_seller=False, is_active=True)
                processing = Order.objects.filter(o_status='In Process')
                delivered = Order.objects.filter(o_status='Delivered')
                deliveredcount = delivered.count()
                processingcount = processing.count()
                customercount = customer.count()
                ordercount = order.count()
                monthordercount = monthOrder.count()
                monthcustomercount = monthCustomers.count()
                todaycustomercount = todayCustomers.count()
                todayordercount = todayOrders.count()
                if order and customer is not None:
                    data = {
                        'ordercount' : ordercount,
                        'customercount' : customercount,
                        'monthorders' : monthordercount,
                        'monthcustomers' : monthcustomercount,
                        'todayorders' : todayordercount,
                        'todaycustomers' : todaycustomercount,
                        'processing' : processingcount,
                        'delivered' : deliveredcount
                    }
                    return Response({
                        'data' : data,
                        'error' : False,
                    })
                return Response({
                    'error' : True,
                    'msg' : 'No info Found'
                })
            
class SellerDashboardView(APIView):
    def get(self, request, id):
            current_month = timezone.now().month
            current_year = timezone.now().year
            current_date = timezone.now().date()
            user = UserDetails.objects.get(id=id, is_seller=True)
            if user is None:
                return Response({
                'error' : True,
                'data' : 'User Not Found'
            })
            else:
                order = OrderDetails.objects.filter(product__user_data__id=id)
                revenue = int(0)
                for bill in order:
                    revenue += int(bill.order.bill_payed)
                todayOrders = OrderDetails.objects.filter(product__user_data__id=id , updated_at__date=current_date)
                todayRevenue = int(0)
                for bill in todayOrders:
                    todayRevenue += int(bill.order.bill_payed)
                monthOrder = OrderDetails.objects.filter(product__user_data__id=id , updated_at__month=current_month, updated_at__year=current_year)
                monthRevenue = int(0)
                for bill in monthOrder:
                    monthRevenue += int(bill.order.bill_payed)
                processing = OrderDetails.objects.filter(product__user_data__id=id , order__o_status='In Process')
                delivered = OrderDetails.objects.filter(product__user_data__id=id , order__o_status='Delivered')
                deliveredcount = delivered.count()
                processingcount = processing.count()
                ordercount = order.count()
                monthordercount = monthOrder.count()
                todayordercount = todayOrders.count()
                if order is not None:
                    data = {
                        'ordercount' : ordercount,
                        'revenue' : revenue,
                        'monthorders' : monthordercount,
                        'monthRevenue' : monthRevenue,
                        'todayorders' : todayordercount,
                        'todayRevenue' : todayRevenue,
                        'processing' : processingcount,
                        'delivered' : deliveredcount
                    }
                    return Response({
                        'data' : data,
                        'error' : False,
                    })
                return Response({
                    'error' : True,
                    'msg' : 'No info Found'
                })
            
def generate_random_code(length):
    characters = string.digits  # Use digits for a numeric code
    code = ''.join(random.choice(characters) for _ in range(length))
    return code  

class ForgotPasswordView(APIView):


    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = UserDetails.objects.get(email=request.data['email'])
            except UserDetails.DoesNotExist:
                return Response({
                    'error': True,
                    'msg': 'User with this email does not exist.'
                }, status=status.HTTP_404_NOT_FOUND)

            reset_code = generate_random_code(6)
            request.session['code'] = reset_code

            # subject = "Password Reset Code"
            # message = f"Your password reset code is: {reset_code}"
            # from_email = "mabuhurairah07@gmail.com"  # Replace with your email
            # recipient_list = [user.email]

            # send_mail(subject, message, from_email, recipient_list)

            return Response({
                'error': False,
                'msg': 'Password reset code has been sent to your email.',
                'code' : reset_code,
            }, status=status.HTTP_200_OK)

        return Response({
            'error': True,
            'msg': 'Invalid data.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
class CheckCodeView(APIView):

    def post(self, request):
        serializer = CodeSerializer(data=request.data)
        if serializer.is_valid():
            sessionCode = request.session.get('code')
            code = request.data['code']
            if sessionCode == code:
                return Response({
                    'data' : 'Validated',
                    'error' : False,
                })
            else:
                return Response({
                    'data' : 'Invalid Code Please Enter Right Code',
                    'error' : True
                })