from rest_framework import serializers
from .models import User, OTP
from django.utils import timezone
from datetime import timedelta

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password', 'age', 'gender')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        # Create the user
        user = User.objects.create_user(**validated_data)
        
        # Create and send OTP after registration
        otp_instance = OTP.objects.create(user=user)
        otp_instance.send_otp()  # Assuming this method sends the OTP to the user's email
        
        return user


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data['email']
        otp = data['otp']
        try:
            otp_record = OTP.objects.get(user__email=email, otp=otp)
            # Optionally, you can add checks for expiration here
        except OTP.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP or email.")
        
        data['user'] = otp_record.user  # Attach the user to the validated data
        return data


class UserDeleteSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User with this ID does not exist.")
        return value
    
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'gender', 'age']