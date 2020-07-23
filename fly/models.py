from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from fish.models import Fish
from river.models import River

NYMPH = 'Nymph',
DRY = 'Dry',
STREAMER = 'Streamer'

FLY_TYPES = (
    (NYMPH, 'Nymph Fly'),
    (DRY, 'Dry Fly'),
    (STREAMER, 'Streamer')
)


class Fly(models.Model):
    type = models.CharField(choices=FLY_TYPES, default=NYMPH, max_length=20)
    image = ProcessedImageField(
        upload_to="user_photos",
        format="JPEG",
        options={"quality": 90},
        processors=[ResizeToFit(width=1200, height=1200)]
    )
    time_of_year = models.DateField()
    quantity = models.IntegerField()
    fish = models.ManyToMany(Fish, on_delete=models.CASCADE)
    river = models.ManyToMany(River, on_delete=models.CASCADE)
