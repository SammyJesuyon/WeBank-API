from django.urls import path
from .views import SpecificTransactionHistory, AllTransactionHistory, MakeTransactionView

urlpatterns = [
    path('api/v1/users/<int:pk>/transaction/', AllTransactionHistory.as_view()),
    path('api/v1/users/transaction/<int:pk>/', SpecificTransactionHistory.as_view()),
    path('api/v1/users/transaction/create/', MakeTransactionView.as_view())
]
