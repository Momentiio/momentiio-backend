from graphene import NonNull, String, List, Int, ID
from graphene_django import DjangoObjectType
from django.core.validators import URLValidator
from ..models import Image


class ImageType(DjangoObjectType):
    class Meta:
        model = Image
