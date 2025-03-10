from django.db import models

from distutils.command.upload import upload
from enum import unique
from random import choices
from django.db import models
import email
from email.policy import default
from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
import uuid
from django.conf import settings
from cloudinary.models import CloudinaryField
from .validators import minimum_amount
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(UserManager):
    use_in_migrations = True
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password):
        """
        Create and save a SuperUser with the given email and password.
        """
        user = self.create_user(email=email, password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = False
        user.save(using=self.db)
        return user

class User(AbstractUser):
    username = None
    USER_TYPE = [
        ( 'Tenant', 'Tenant'),
        ('Agent','Agent')
    ]
    entry = models.CharField(choices=USER_TYPE, max_length=10)
    email = models.EmailField(_('email address'), unique=True)
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    name = models.CharField(max_length=20, blank=True, null=True, verbose_name='Full Name')
    image = models.ImageField(upload_to = 'profile/', blank=True)
    home_address = models.CharField( max_length=30, null=True,  blank=True)
    balance = models.FloatField(default=0, validators=[minimum_amount, ])
    country = CountryField()
    phone_number = PhoneNumberField(null=True, blank=True, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser



        