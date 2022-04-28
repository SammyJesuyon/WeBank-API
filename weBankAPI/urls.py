from django.urls import path
from .views import (
    SpecificTransactionHistory,
    AllTransactionHistory,
    AccountInfo,
    RegisterUser,
    VerifyEmail,
    AccountCreation,
    LoginView
)

urlpatterns = [
    path('api/v1/users/register/', RegisterUser.as_view()),
    path('api/v1/users/verify-email/', VerifyEmail.as_view()),
    path('api/v1/users/login/', LoginView.as_view()),
    path('api/v1/users/create-account/', AccountCreation.as_view()),
    path('api/v1/users/<int:pk>/transaction/', AllTransactionHistory.as_view()),
    path('api/v1/users/transaction/<int:pk>/', SpecificTransactionHistory.as_view()),
    path('api/v1/users/<int:pk>/account/', AccountInfo.as_view(),)
]
