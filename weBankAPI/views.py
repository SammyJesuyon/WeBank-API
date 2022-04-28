from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
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

        OTP = Util.generate_otp()

        user.otp = OTP
        user.save()

        absurl = str(OTP)

        email_body = 'Hi ' + user.username + ' use the OTP to verify your email ' + absurl

        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'verify your email'}

        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)
    
class UserListView(generics.ListAPIView):
    queryset= User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
class UserDetailsView(generics.RetrieveAPIView):
    queryset= User.objects.filter()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
     
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
        
        

class LogoutView(generics.GenericAPIView):
    # authentication_classes = [TokenAuthentication]
    
    def get(self, request):
        del request.user.token
        
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'logout successful'
        }
        return response

    
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
    

class ResetPasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ResetPasswordSerializer
    model = User
    # permission_classes = (IsAuthenticated)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'message': 'Password updated successfully',
            }

            return Response(data=response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    