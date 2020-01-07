import secrets
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

from core.models import BaseModel
from core.mixins import TimestampMixin


def invitation_expiration():
    return timezone.now() + timezone.timedelta(days=settings.INVITE_USER_EXPIRATION)


class Invite(BaseModel, TimestampMixin):
    token = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(blank=False, max_length=100)
    last_name = models.CharField(blank=False, max_length=100)
    email = models.EmailField(blank=True, unique=True)
    phone_number = PhoneNumberField(null=True, blank=True, unique=True)
    avatar = ProcessedImageField(
        upload_to="user_photos",
        format="JPEG",
        options={"quality": 90},
        processors=[ResizeToFit(width=1200, height=1200)],
        blank=True,
        null=True
    )
    note = models.TextField(max_length=250, blank=True)
    sponsor = models.UUIDField(blank=False)
    expiration = models.DateTimeField(
        default=invitation_expiration)

    def __str__(self):
        return f"{self.first_name}"

    @property
    def is_expired(self):
        invite_exp = self.expiration > timezone.now()
