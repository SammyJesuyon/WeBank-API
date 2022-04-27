from django.urls import path
from .views import ClientAccountTransactionHistory

urlpatterns = [
    path('client/transaction/history', ClientAccountTransactionHistory.as_view()),
]
