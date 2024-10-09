"""Handle the url pattern for the user authentication"""
from django.urls import path

# for refresh token
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (RegisterUserView,
                    VerifyUserEmail,
                    ResendOTP,
                    LoginUserView,
                    TestAuthenticationView, PasswordResetConfirm,
                    SetNewPassword, PasswordResetRequestView, 
                    LogoutUserView)

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify-email/', VerifyUserEmail.as_view(), name='verify'),
    path('resend-otp/', ResendOTP.as_view(), name='resend-otp'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password-reset-confirm'),
    path('set-new-password/', SetNewPassword.as_view(), name='set-new-password'),
    path('test-profile/', TestAuthenticationView.as_view(), name='granted'),
    path('logout/', LogoutUserView.as_view(), name='logout'),

    # handle token refresh
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
]
