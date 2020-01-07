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
from invites.models import Invite


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
    phone_number = PhoneNumberField(null=True, unique=True)
    sponsor = models.UUIDField(
        blank=False, null=False, default="f0a066f6-2281-468e-bdba-2ca79db5e9b4")
    invites = models.ManyToManyField(
        Invite, related_name="invites")
    is_hidden = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username}"

    @property
    def full_name(self):
        return ' '.join(filter(bool, (self.first_name, self.last_name)))


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
