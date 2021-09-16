from datetime import datetime

import cloudinary
import jwt
from cloudinary.models import CloudinaryField
from django.conf import settings
from django.conf.global_settings import SECRET_KEY
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin, UserManager)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models.signals import (post_delete, post_save, pre_delete,
                                      pre_save)
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from _datetime import timedelta
from helpers.models import TrackingModel
from helpers.utils import unique_user_slug_generator

"""
- Add new properties access_token
- Verify email
- User email & password instead of username/password
"""


GENDER_CHOICE = (("Male", "Male"), ("Female", "Female"))


class MyUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin, TrackingModel):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, Email and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        blank=False,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    slug = models.SlugField(unique=True)
    bio = models.TextField(
        _('user_bio'),
        max_length=240,
        blank=True,
        null=True,
        default=""
    )
    avatar = CloudinaryField(
        folder='UsersImages',
        blank=True,
        null=True,
        help_text=_("You profile image"),
        transformation={"quality": "auto:eco"},
        resource_type="image",
    )
    # avatar = models.ImageField(storage=PublicMediaStorage(), upload_to=upload_dir, null=True, blank=True,
    #
    first_name = models.CharField(_('first name'), max_length=150, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    email = models.EmailField(_('email address'), blank=False, unique=True)
    gender = models.CharField(_('gender'), max_length=6, choices=GENDER_CHOICE, blank=True, null=True)
    follow_count = models.PositiveIntegerField(default=0)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    email_verified = models.BooleanField(
            ('email_verified'),
            default=False,
            help_text=(
                "Designates whether this user's email is verified."
            ),
        )
    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f"{self.username}"

    @property
    def image_url(self):
        if self.avatar:
            return f"{self.avatar}"
        return 'https://res.cloudinary.com/geetechlab-com/image/upload/v1583147406/nwaben.com/user_azjdde_sd2oje.jpg'

    @property
    def token(self):
        return jwt.encode(
            {
                "username": self.username,
                "email": self.email,
                "exp":datetime.utcnow() + timedelta(hours=24)
            },
            settings.SECRET_KEY,
            algorithm="HS256"
        )


@receiver(pre_save, sender=User)
def user_pre_save_signal(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_user_slug_generator(instance)


@receiver(pre_delete, sender=User)
def user_avatar_delete(sender, instance, **kwargs):
    cloudinary.uploader.destroy(instance.avatar.public_id)
