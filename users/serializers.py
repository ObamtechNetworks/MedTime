"""Serializes the user model"""
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from .models import User

class UserRegisterationSerializer(serializers.ModelSerializer):
    """Serializes user to be created during registration"""
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    confirm_password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        """Handles the Meta data to be exposed for the specified model
        """
        model=User
        fields=['email', 'first_name', 'last_name', 'password', 'confirm_password']

    def validate(self, attrs):
        """handles fields / attributes validations using the specified model
        our case: User model
        """
        password = attrs.get('password', '')
        confirm_password = attrs.get('confirm_password', '')
        if password != confirm_password:
                    raise serializers.ValidationError(_('Passwords do not match'))
        return attrs

    def create(self, validated_data):
        """Handles user creation after data has been validated"""
        user = User.objects.create_user(
              email=validated_data['email'],
              first_name=validated_data['first_name'],
              last_name=validated_data['last_name'],
              password=validated_data['password']  # this is hashed password
        )
        return user
