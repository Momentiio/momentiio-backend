from graphene import NonNull, String, List, Int, ID
from graphene_django import DjangoObjectType
from django.core.validators import URLValidator
from ..models import Image, Filter


class FilterType(DjangoObjectType):
    class Meta:
        model = Filter
        only_fields = {
            'name',
            'image_filter',
            'background',
            'blend_mode',
            'opacity'
        }


class ImageType(DjangoObjectType):
    url = String()
    image_filter = String()

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

    def resolve_image_filter(self, info):
        return Image.image_filter(name=image_filter)
