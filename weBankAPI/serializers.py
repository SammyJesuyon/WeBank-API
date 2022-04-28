from rest_framework import serializers
from .models import Accounts
from .models import *
from rest_framework import serializers
from rest_framework.authtoken.models import Token

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ['id','fullname','account_no', 'account_type']
    
    
class AccountCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ['fullname','account_type']


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email',)
       

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
        email=validated_data['email'],
        username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user
    

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    
    
class EmailVerification(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'otp']
        
        
class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


