import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


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


class User(BaseModel, AbstractUser):
    """Custom user model."""


class Post(BaseModel):
    user = models.ForeignKey(
        User, verbose_name="Created By", on_delete=models.CASCADE, related_name="user_photos"
    )
    caption = models.TextField(max_length=500, blank=True)
    photo = ProcessedImageField(
        upload_to="user_photos",
        format="JPEG",
        options={"quality": 90},
        processors=[ResizeToFit(width=1200, height=1200)],
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s Photo on {self.date_created}"

    class Meta:
        """Metadata."""

        ordering = ["-date_created"]


class Like(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="likes")
    photo = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="likes")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} Like"

    class Meta:
        unique_together = (("user", "photo"))
        ordering = ["-date_created"]


class Comment(BaseModel):
    """A comment on a post."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")
    photo = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")

    content = models.TextField(max_length=2000)

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        """Metadata."""

        ordering = ["-date_created"]
