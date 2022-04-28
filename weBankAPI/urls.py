from django.urls import path,include
from .views import (
    SpecificTransactionHistory,
    AllTransactionHistory,
    MakeTransactionView,
    AccountInfo,
    RegisterUser,
    VerifyEmail,
    UserListView,
    UserDetailsView
)

urlpatterns = [
    path('api/v1/users/register/', RegisterUser.as_view(),name='create-user'),
    path('api/v1/users/all/', UserListView.as_view()),
    path('api/v1/users/<int:pk>/', UserDetailsView.as_view()),
    path('api/v1/users/verify-email/', VerifyEmail.as_view()),
    path('api/v1/users/<int:pk>/transaction/', AllTransactionHistory.as_view()),
    path('api/v1/users/transaction/<int:pk>/', SpecificTransactionHistory.as_view()),
    path('api/v1/users/transaction/create/', MakeTransactionView.as_view()),
    path('api/v1/users/<int:pk>/account/', AccountInfo.as_view()),
    path('api/v1/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
