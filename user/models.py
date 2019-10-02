from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

from core.models import BaseModel
from interests.models import Interest
from address.models import Address


class Profile(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
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
        return '%s %s' % (self.user.first_name, self.user.last_name)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# Create Address Fields on user creation
# @receiver(post_save, sender=User)
# def create_user_address(sender, instance, created, **kwargs):
#     if created:
#         Address.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_address(sender, instance, **kwargs):
#     instance.address.save()
