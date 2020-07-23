from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from fish.models import Fish


class River(models.Model):
    location = models.CharField()
    title = models.CharField(max_length=150, required=True)
    image = ProcessedImageField(
        upload_to="user_photos",
        format="JPEG",
        options={"quality": 90},
        processors=[ResizeToFit(width=1200, height=1200)],
    )
    fish = models.ForeignKey(Fish, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"
