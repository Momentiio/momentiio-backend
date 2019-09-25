import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .mixins import AddressModelMixin
from interests.models import Interest


class BaseModel(models.Model):
    """Base model for the application. Uses UUID for pk."""
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )

    class Meta:
        """Metadata."""
        abstract = True


class Profile(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=1200, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    interests = models.ManyToManyField(Interest)
    postal_address = AddressModelMixin()

    def __str__(self):
        return f"{self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
