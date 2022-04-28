from django.shortcuts import render,HttpResponse
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import generics, viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.conf import settings
from django.contrib.auth import authenticate, login
from .utils import Util



class RegisterUser(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])

        OTP = Util.generate_otp(6)

        user.otp = OTP
        user.save()

        absurl = str(OTP)

        email_body = 'Hi ' + user.username + ' use the OTP to verify your email ' + absurl

        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'verify your email'}

        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)
    
class VerifyEmail(generics.GenericAPIView):
    serializer_class = EmailVerification

    def post(self, request):
        data = request.data
        otp = data.get('otp', '')
        email = data.get('email', '')
        if otp is None or email is None:
            return Response(data=dict(invalid_input="Please provide both otp and email"),
                            status=status.HTTP_400_BAD_REQUEST)
        get_user = User.objects.filter(email=email)
        if not get_user.exists():
            return Response(data=dict(invalid_email="please provide a valid registered email"),
                            status=status.HTTP_400_BAD_REQUEST)
        user = get_user[0]
        if user.otp != otp:
            return Response(data=dict(invalid_otp="please provide a valid otp code"),
                            status=status.HTTP_400_BAD_REQUEST)
        user.is_verified = True
        user.save()
        return Response(data={
            "success": "Your account has been successfully verified"
        }, status=status.HTTP_200_OK)
        
class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email', '')
        password = request.data.get('password', '')

        if email is None or password is None:
            return Response(data={'Invalid_credentials': 'Please provide email and password'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
        if not user:
            return Response(data={'invalid_credentials': 'Ensure email and password are correct and you have '
                                                         'verified your account'}, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_verified:
            return Response(data={'invalid_credentials': 'Please verify your account'},
                            status=status.HTTP_400_BAD_REQUEST)
        self.serializer_class(user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'token': token.key, 'success': "You've successfully Logged in"},
                        status=status.HTTP_200_OK)
        
        
class AccountCreation(generics.GenericAPIView):
    serializer_class = AccountCreationSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = User.objects.get(email=request.user.email)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            firstname = serializer.validated_data['firstname']
            lastname = serializer.validated_data['lastname']
            account_type = serializer.validated_data['account_type']
            account_number = Util.create_account_number(7)
            try:
                account_creation = Accounts(
                    user=user, 
                    firstname=firstname,
                    lastname=lastname,
                    account_type=account_type,
                    account_no=account_number,
                )
                return Response(data={'success': 'Account successfully created,',
                                      'account_type': f' {account_type}',
                                      'account_number': f'{account_number}'},
                                status=status.HTTP_202_ACCEPTED)

            except Exception as error:
                if Accounts.objects.get(user_id=user):
                    return Response({'error': 'You already have an account'}, status=status.HTTP_400_BAD_REQUEST)
                return Response(data={'error': error}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data={'error': 'Something Went Wrong'}, status=status.HTTP_400_BAD_REQUEST)
    
class AllTransactionHistory(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    
class SpecificTransactionHistory(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class AccountInfo(generics.RetrieveAPIView):
    queryset = Accounts.objects.all()
    serializer_class = AccountSerializer
    