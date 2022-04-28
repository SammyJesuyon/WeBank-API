from django.shortcuts import render,HttpResponse
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django.conf import settings
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
    
class AllTransactionHistory(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    
class SpecificTransactionHistory(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    
class MakeTransactionView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

class AccountInfo(generics.RetrieveAPIView):
    queryset = Accounts.objects.all()
    serializer_class = AccountSerializer
    