from django.urls import path,include
from .views import (
    SpecificTransactionHistory,
    AllTransactionHistory,
    AccountInfo,
    RegisterUser,
    VerifyEmail,
<<<<<<< HEAD
    AccountCreation,
    LoginView,
    LogoutView,
    CreateTransaction
=======
    UserListView,
    UserDetailsView
>>>>>>> 37b6e87effc5771f87b1fe1aee991348f0770d2b
)

urlpatterns = [
    path('api/v1/users/register/', RegisterUser.as_view(),name='create-user'),
    path('api/v1/users/all/', UserListView.as_view()),
    path('api/v1/users/<int:pk>/', UserDetailsView.as_view()),
    path('api/v1/users/verify-email/', VerifyEmail.as_view()),
    path('api/v1/users/login/', LoginView.as_view()),
    path('api/v1/users/logout/', LogoutView.as_view()),
    path('api/v1/users/create-account/', AccountCreation.as_view()),
    path('api/v1/users/create-transaction/', CreateTransaction.as_view()),
    path('api/v1/users/<int:pk>/transaction/', AllTransactionHistory.as_view()),
    path('api/v1/users/transaction/<int:pk>/', SpecificTransactionHistory.as_view()),
<<<<<<< HEAD
    path('api/v1/users/<int:pk>/account/', AccountInfo.as_view(),)
=======
    path('api/v1/users/transaction/create/', MakeTransactionView.as_view()),
    path('api/v1/users/<int:pk>/account/', AccountInfo.as_view()),
    path('api/v1/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
>>>>>>> 37b6e87effc5771f87b1fe1aee991348f0770d2b
]
