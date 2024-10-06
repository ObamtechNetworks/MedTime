"""Handles the api views for the user model"""

# standard imports
from datetime import timedelta
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# rest frame works modules
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated, AllowAny
import pyotp

# import all serializers for user
from .serializers import (UserRegisterationSerializer,
                        #   LoginSerializer, PasswordResetRequestSerializer,
                        #   SetNewPasswordSerializer,
                        #   LogoutUserSerializer
                          )

from .utils import send_code_to_user
from .models import User, OneTimePassword

# Using class based views, specifically GenericAPIView
class RegisterUserView(GenericAPIView):
    """the config for the register endpoint for our api

    Args:
        GenericAPIView (clas): generic api from rest_framework
    """
    serializer_class = UserRegisterationSerializer

    # define a post method
    def post(self, request):
        """a post request to be processed for the register endpoint
        sends an email to the user after registeration

        Args:
            request (method): request method to fetch data
        """
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        # check if serialized data from user data is valid
        if serializer.is_valid(raise_exception=True):
            # if valid save the data
            serializer.save()
            user = serializer.data
            # send email function user['emial']  # utils module
            send_code_to_user(user['email'])
            return Response({
                'data': user,
                'message': f"Hi {user.get('first_name')} thanks for signing up, a passcode has been sent to your mail, use it to complete your registration ..."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class VerifyUserEmail(GenericAPIView):
#     """Verifies user email based on the OTP code sent."""

#     def post(self, request):
#         """Handles POST request to verify user using the OTP."""
#         # store request in a payload
#         payload = request.data

#         # extract each contents
#         otp_code = payload.get('otp')
#         email = payload.get('email')

#         if not otp_code or not email:
#             return Response({'message': 'OTP code and email are required'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = User.objects.get(email=email)
#             otp_obj = OneTimePassword.objects.get(user=user, otp_code=otp_code)

#             # Verify the OTP
#             totp = pyotp.TOTP(otp_obj.otp_secret, interval=300)
#             if totp.verify(otp_code):
#                 # Check if the OTP has expired
#                 if otp_obj.created_at < timezone.now() - timedelta(minutes=5):
#                     #delete otp obj
#                     otp_obj.delete()
#                     user.save()
#                     return Response({'message': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)
                
#                 # Verify the user
#                 if not user.is_verified:
#                     user.is_verified = True
#                     otp_obj.delete()
#                     user.save()
#                     return Response({'message': 'Account email verified successfully'}, status=status.HTTP_200_OK)
#                 else:
#                     return Response({'message': 'User email is already verified'}, status=status.HTTP_204_NO_CONTENT)
#             else:
#                 return Response({'message': 'Invalid or expired OTP code'}, status=status.HTTP_400_BAD_REQUEST)
        
#         except User.DoesNotExist:
#             return Response({'message': 'Invalid email'}, status=status.HTTP_404_NOT_FOUND)
#         except OneTimePassword.DoesNotExist:
#             return Response({'message': 'Invalid OTP code'}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class ResendOTP(GenericAPIView):
#     """Handles requests to resend the OTP to the user's email."""
    
#     def post(self, request):
#         email = request.data.get('email')
        
#         if not email:
#             return Response({'message': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = User.objects.get(email=email)
#             send_code_to_user(user)
#             return Response({'message': 'A new OTP has been sent to your email.'}, status=status.HTTP_200_OK)
        
#         except User.DoesNotExist:
#             return Response({'message': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
#         except ValueError as e:
#             return Response({'message': str(e)}, status=status.HTTP_429_TOO_MANY_REQUESTS)
#         except Exception as e:
#             return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# class LoginUserView(GenericAPIView):
#     """handles login endpoint

#     Args:
#         GenericAPIView (class): generic apiview
#     """
#     serializer_class = LoginSerializer
    
#     def post(self, request):
#         """sends a post request and process user's login

#         Args:
#             request (method): sends a post request
#         """
#         serializer = self.serializer_class(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
# class TestAuthenticationView(GenericAPIView):
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request):
#         data = {'msg': 'It works'}
#         return Response(data, status=status.HTTP_200_OK)


# class PasswordResetRequestView(GenericAPIView):
#     serializer_class = PasswordResetRequestSerializer
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data, context={'request': request})
#         # Assuming 'email' is a field in your serializer
#         serializer.is_valid(raise_exception=True)
#         email = serializer.validated_data['email']
#         return Response({
#             'message': f'A link has been sent to {email} to reset your password.'
#         }, status=status.HTTP_200_OK)
        
# # from frontend, when user clicks on the reset password link, it will take them to route to this view 
# class PasswordResetConfirm(GenericAPIView):
#     def get(self, request, uidb64, token):
#         try:
#             # first extract the user id
#             user_id = smart_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(id=user_id)
#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 return Response({
#                     'message': 'token is invalid or has expired'
#                 }, status=status.HTTP_401_UNAUTHORIZED)
#             return Response({
#                 'success': True,
#                 'message': 'crendentials is valid',
#                 'uidb64': uidb64,
#                 'token':token
#             }, status=status.HTTP_200_OK)
#         except DjangoUnicodeDecodeError:
#             return Response({
#                     'message': 'token is invalid or has expired'
#                 }, status=status.HTTP_401_UNAUTHORIZED)

# # after confirming password, this view is shown to set new password
# class SetNewPassword(GenericAPIView):
#     serializer_class = SetNewPasswordSerializer
#     # send a patch request
#     def patch(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # serializer.validate(serializer.data)
#         return Response({
#             'message': 'password has been reset successfully'
#         }, status=status.HTTP_200_OK)
        

# class LogoutUserView(GenericAPIView):
#     serializer_class = LogoutUserSerializer
#     permission_classes = [AllowAny]
    
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'success': 'You have been logged out successfully'}, status=status.HTTP_200_OK)
