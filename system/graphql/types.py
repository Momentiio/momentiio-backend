from graphene import NonNull, Field, String, List, Int, ID
from graphene_django import DjangoObjectType
from django.core.validators import URLValidator
from ..models import Image, Filter


class ImageFilterType(DjangoObjectType):
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

    class Meta:
        model = Image

    def resolve_url(self, info):
        return Image.get_absolute_url(self)
