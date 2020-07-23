from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
# Create your models here.
RAINBOWTROUT = 'Rainbow Trout',
BROWNTROUT = 'Brown Trout',
BROOKETROUT = 'Brooke Trout',
TIGERTROUT = 'Tiger Trout',
LAKETROUT = 'Lake Trout',
WHITEFISH = 'White Fish',
GRAYLING = 'Grayling'

FISH_SPECIES = (
    (RAINBOWTROUT, 'Rainbow Trout'),
    (BROWNTROUT, 'Brown Trout'),
    (BROOKETROUT, 'Brooke Trout'),
    (TIGERTROUT, 'Tiger Trout'),
    (LAKETROUT, 'Lake Trout'),
    (WHITEFISH, 'White Fish'),
    (GRAYLING, 'Grayling'),
)


class Fish(models.Model):
    species = models.CharField(
        choices=FISH_SPECIES, default=RAINBOWTROUT, max_length=50)
    size = models.CharField()
    image = ProcessedImageField(
        upload_to="user_photos",
        format="JPEG",
        options={"quality", 90},
        processors=[ResizeToFit(width=1200, height=1200)]
    )
