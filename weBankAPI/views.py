from django.shortcuts import render,HttpResponse
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly



class ClientAccountTransactionHistory(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    
