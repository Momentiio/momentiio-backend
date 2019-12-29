from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from phonenumber_field.modelfields import PhoneNumberField
from core.models import BaseModel
from core.mixins import TimestampMixin
from interests.models import Interest


def invitation_expiration():
    return timezone.now() + timezone.timedelta(days=12)


class InviteUser(BaseModel, TimestampMixin):
    sponsor = models.CharField(default='0', editable=False, max_length=30)
    name = models.CharField(blank=False, max_length=100)
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
    expiration = models.DateTimeField(
        default=invitation_expiration)

    def __str__(self):
        return f"{self.name}"


class UserModel(AbstractUser, BaseModel,  TimestampMixin):
    AFFILIATE_USER = 'AFF'
    GENERIC_USER = 'CUS'

    USER_TYPES = (
        (AFFILIATE_USER, 'Affiliate'),
        (GENERIC_USER, 'Customer')
    )
    # User Fields
    type = models.CharField(
        choices=USER_TYPES, default=GENERIC_USER, max_length=5)
    username = models.CharField(max_length=30, unique=True)
    phone_number = PhoneNumberField(null=True, blank=False, unique=True)
    sponsor = models.PositiveIntegerField(
        editable=False, blank=False, default=1)
    invites = models.ManyToManyField(
        InviteUser, related_name="invites")
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}"

    @property
    def full_name(self):
        return ' '.join(filter(bool, (self.user.first_name, self.user.last_name)))


class Profile(BaseModel):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name="profile")
    profile_avatar = ProcessedImageField(
        upload_to="user_photos",
        format="JPEG",
        options={"quality": 90},
        processors=[ResizeToFit(width=1200, height=1200)],
        blank=True,
        null=True
    )
    bio = models.TextField(max_length=1200, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    interests = models.ManyToManyField(Interest)
    is_private = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}"

    @property
    def full_name(self):
        "Returns the person's full name."
        return user.get_full_name()


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
