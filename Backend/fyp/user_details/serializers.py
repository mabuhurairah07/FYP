from rest_framework import serializers
from .models import UserDetails
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = '__all__'

class AdminDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['id','username', 'email', 'phone_no']
        
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = UserDetails
        fields = ['id','username', 'email', 'password', 'phone_no']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField() 
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")
        if not username or not password:
            raise serializers.ValidationError("Both Fields are required")
        return data
    
class SellerSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = UserDetails
        fields = ['id','username', 'email', 'password', 'phone_no']

class SellerLoginSerializer(serializers.Serializer):
    username = serializers.CharField() 
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")
        if not username or not password:
            raise serializers.ValidationError("Both Fields are required")
        return data
    
class AdminSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = UserDetails
        fields = ['id','username', 'email', 'password', 'phone_no']

class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField() 
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")
        if not username or not password:
            raise serializers.ValidationError("Both Fields are required")
        return data
