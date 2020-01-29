from graphene import NonNull, String, List, Int, ID
from graphene_django import DjangoObjectType
from django.core.validators import URLValidator
from ..models import Image


class ImageType(DjangoObjectType):
    url = String()

    class Meta:
        model = Image
        only_fields = {
            'id',
            'image_height',
            'image_width',
            'uploaded_at'
        }

    def resolve_url(self, info):
        return Image.get_absolute_url(self)
