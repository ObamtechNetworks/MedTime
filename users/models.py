"""Model for the user"""
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .manager import UserManager

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    """Create a custom User class

    Args:
        AbstractBaseUser (class): extends its functionality for the User class
        PermissionsMixin (class): extends permission functionality for user
    """
    email = models.EmailField(max_length=255, unique=True, verbose_name="Email Address")
    first_name = models.CharField(max_length=255, verbose_name="First Name")
    last_name = models.CharField(max_length=255, verbose_name="Last Name")
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()


    def __str__(self) -> str:
        return self.full_name

    @property
    def full_name(self) -> str:
        """Returns the user's full name."""
        return f"{self.first_name} {self.last_name}"

    def tokens(self):
        """to handle the json webtoken authentication
        """
        # refresh = RefreshToken.for_user(self)
        # return {
        #     'refresh': str(refresh),
        #     'access': str(refresh.access_token)
        # }

class OneTimePassword(models.Model):
    """One time password model for saving otp into data for each specific user
    Args:
        models (class): extends the django class model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_secret = models.CharField(max_length=32, unique=True)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # pylint: disable=no-member
        return f"{self.user.email} - {self.otp_code}"
