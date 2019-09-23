from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from orderable.models import Orderable


class Category(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.title}"


class Interest(Orderable):
    title = models.CharField(max_length=100)
    photo = ProcessedImageField(
        upload_to="interest_photos",
        format="JPEG",
        options={"quality": 90},
        processors=[ResizeToFit(width=1200, height=1200)],
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"
