from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']  # Assuming you save the user in the serializer
            token, created = Token.objects.get_or_create(user=user)  # Get or create a token for the user
            return Response({"message": "OTP verified. Login successful.", "token": token.key}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserDeleteView(APIView):

#     def delete(self, request):
#         permission_classes = [AllowAny]
#         serializer = UserDeleteSerializer(data=request.data)
#         if serializer.is_valid():
#             user_id = serializer.validated_data['user_id']
#             user = get_object_or_404(User, id=user_id)
#             user.delete()
#             return Response({"message": "User deleted successfully."}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDeleteView(APIView):
    permission_classes = [AllowAny]  # Allow unrestricted access for deletion

    def delete(self, request):
        serializer = UserDeleteSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            user = get_object_or_404(User, id=user_id)
            user.delete()
            return Response({"message": "User deleted successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    User = get_user_model()

# user list
class UserDetailView(RetrieveAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated] 
    def get_object(self):
        # Return the currently authenticated user
        return self.request.user