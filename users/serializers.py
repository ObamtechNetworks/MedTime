"""Serializes the user model"""
import os
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, smart_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.exceptions import AuthenticationFailed

from users.utils import send_normal_email
from .models import User

class UserRegisterationSerializer(serializers.ModelSerializer):
    """Serializes user to be created during registration"""
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    confirm_password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        """Handles the Meta data to be exposed/expected for the specified model
        """
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'confirm_password']

    def validate(self, attrs):
        """handles fields / attributes validations using the specified model
        our case: User model
        """
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
                    raise serializers.ValidationError(detail={'password':"passwords does not match"})
        return super().validate(attrs)

    def create(self, validated_data):
        """Handles user creation after data has been validated"""
        validated_data.pop('confirm_password')

        user = User.objects.create_user(
              email=validated_data['email'],
              first_name=validated_data['first_name'],
              last_name=validated_data['last_name'],
              password=validated_data['password']  # this is hashed password
        )
        return user


class LoginSerializer(serializers.ModelSerializer):
    """serializes user login data

    Args:
        serializers (class): django rest_framework serializer class
    """
    email = serializers.EmailField(max_length=255, min_length=6)
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    full_name = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'full_name', 'access_token', 'refresh_token']
        
    def validate(self, attrs):
        email = attrs.get('email').strip()
        password = attrs.get('password').strip()
        request = self.context.get('request')

        user = authenticate(request, email=email, password=password)  # lookup db if user with data exists
        if not user:
            raise AuthenticationFailed("invalid credentials try again")
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified")

        user_token = user.tokens()  # generates the access token and referesh token for user
        return {
            'email': user.email, 
            'full_name': user.full_name,  # gets user full name
            'access_token': str(user_token.get('access')),
            'refresh_token': str(user_token.get('refresh'))
        }
        
class PasswordResetRequestSerializer(serializers.Serializer):
    """password resetting

    Args:
        serializers (class): extends serialization function to model
    """
    email = serializers.EmailField(max_length=255)
    
    # class Meta:
    #     fields = ['email']
        
    # class Meta:
    #     fields = ['email']  # require email from endpoint
        
    def validate(self, attrs):
        email = attrs.get('email')
        if not User.objects.filter(email=email).exists():  #check if user exists
            raise serializers.ValidationError("No user found with this email.")
        # if email exists, then proceed below
        user = User.objects.get(email=email)
        # Encode the user id into a url readable string
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)  # generate token for user

        request = self.context.get('request')  # Get the request from context
        # Get the site domain or use a default frontend domain from environment variables
        frontend_domain = os.getenv('FRONTEND_DOMAIN', get_current_site(request).domain)

        # Determine the protocol (http/https)
        protocol = 'https' if request.is_secure() else 'http'
        # Reverse the 'password-reset-confirm' url with the encoded user id and token as kwargs
        relative_link = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
        # Construct the absolute link with the protocol, domain, and relative link
        absolute_link = f"{protocol}://{frontend_domain}{relative_link}"

        # Prepare the email body
        email_body = f"Hi, use the link below to reset your password:\n{absolute_link}"
        email_data = {
            'email_body': email_body,
            'email_subject': "Reset your Password",
            'to_email': user.email
        }

        # Send the email (handle exceptions in case of failures)
        try:
            send_normal_email(email_data)
        except Exception as e:
            raise serializers.ValidationError(f"Error sending email: {str(e)}")

        return attrs


class SetNewPasswordSerializer(serializers.Serializer):
    """Serialzer for the set new password view"""
    password = serializers.CharField(max_length=100, min_length=8, write_only=True)
    confirm_password = serializers.CharField(max_length=100, min_length=8, write_only=True)
    uidb64 = serializers.CharField(write_only=True)  # to identify the user that wants to change password
    token = serializers.CharField(write_only=True)  # to check if the incoming token is valid

    class Meta:
        fields = ['password', 'confirm_password', 'uidb64', 'token']

    def validate(self, attrs):
        try:
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')

            # decode the uidb64
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            # check if token is still valid
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("Reset link is invalid or has expired")

            # Check for password mismatch
            if password != confirm_password:
                raise serializers.ValidationError({"password": "Passwords do not match"})

            user.set_password(password)  # has the entered password
            user.save()  # save the updated details of user to database

            return user  # return the user
        except Exception as e:
            raise AuthenticationFailed("An unexpected error occurred. Invalid or expired token")


class LogoutUserSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    
    # default error message for TokenError
    default_error_messages = {
        'bad_token': ('Token is invalid or has expired')
    }
    
    def validate(self, attrs):
        refresh_token = attrs.get('refresh_token')
        try:
            RefreshToken.verify(refresh_token)
        except Exception as e:
            raise ValidationError(self.fields['refresh_token'].error_messages['bad_token']) from e
        return attrs
    
    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()  # blacklist the token, more like delete token
        except TokenError:
            return self.fail('bad_token')
