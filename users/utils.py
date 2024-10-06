"""Utility function for handling otp generation"""
# function to generate OTP and send email
# there are different approaches e.g a shortlived otp,
# to use python package pyotp ( this expires at a particular time)
# what we want is just a simple otp verification

from datetime import timedelta
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import pyotp
from .models import User, OneTimePassword

def generate_otp_secret():
    """Generates a random secret key and OTP code for OTP generation."""
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret, interval=300)
    otp = totp.now()
    return secret, otp

def send_code_to_user(email):
    """Send OTP code to user's email using pyotp."""
    subject = "One Time passcode for Email Verification"
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist as error:
        raise ValueError(_("User with the specified email does not exist.")) from error

    otp_obj, created = OneTimePassword.objects.get_or_create(user=user)

    if not created and otp_obj.created_at > timezone.now() - timedelta(minutes=3):
        raise ValueError("An OTP was previously sent. Please check your inbox.")

    otp_secret, otp_code = generate_otp_secret()
    otp_obj.otp_secret = otp_secret
    otp_obj.otp_code = otp_code
    otp_obj.created_at = timezone.now()
    otp_obj.save()


    current_site = "MedTime"
    email_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .email-container {{
                max-width: 600px;
                margin: auto;
                background-color: #ffffff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            .email-header {{
                font-size: 24px;
                font-weight: bold;
                color: #3a6ad6; /* Base color */
            }}
            .email-body {{
                margin-top: 20px;
                font-size: 16px;
                color: #555555; /* Slightly darker for readability */
            }}
            .otp-code {{
                font-size: 20px;
                font-weight: bold;
                color: #007BFF; /* A shade of blue that complements #3a6ad6 */
            }}
            .footer {{
                margin-top: 20px;
                font-size: 12px;
                color: #777777; /* A light gray for footer text */
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="email-header">Thank you for registering an account on {current_site}.</div>
            <div class="email-body">
                Hi {user.first_name},<br><br>
                Thank you for signing up on {current_site}.<br>
                Please use the passcode below to complete your registration:<br><br>
                <div class="otp-code">Verification code: {otp_code}</div><br>
                Please note that this code is only valid for 5 minutes.<br><br>
                Your Health, On Time.
            </div>
            <div class="footer">
                &copy; {current_site} 2024. All rights reserved.
            </div>
        </div>
    </body>
    </html>
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    d_email = EmailMessage(subject=subject, body=email_body, from_email=from_email, to=[email])
    d_email.content_subtype = "html"  # This is important to ensure the email is sent as HTML
    d_email.send(fail_silently=True)


def send_normal_email(data):
    """sends email

    Args:
        data (dict): use the data to send a mail
    """
    email = EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.EMAIL_HOST_USER,
        to=[data['to_email']]
    )
    email.send()
