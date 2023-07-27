from django.shortcuts import render
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Transaction
from .serializers import TransactionSerializer

# Create your views here.
class TransactionView(APIView):
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            transaction_id = request.data['transaction_id']
            created_at = timezone.now()
            updated_at = timezone.now()
            check = Transaction.objects.get(transaction_id=transaction_id)
            if check:
                return Response({'message': 'A Same Id already exists.', 'error' : True}, status=status.HTTP_400_BAD_REQUEST)
            else :
                return Response({'data': serializer.data,'error' : False, 'msg' : 'Transaction Id Added'},status.HTTP_201_CREATED)
        return Response({'message': 'No Id to Add.', 'error' : True}, status=status.HTTP_400_BAD_REQUEST)