from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    # path('login/request-otp/', RequestOTPView.as_view(), name='request-otp'),
    path('login/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('users/', UserDetailView.as_view(), name='user-list'),
    path('delete-user/', UserDeleteView.as_view(), name='delete_user'),
]