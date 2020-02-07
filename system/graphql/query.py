import graphene
from django.db import models
from graphene import Field, List, Int, ID, NonNull, ObjectType
from graphene_django import DjangoObjectType
from ..models import ImageFilter
from .types import ImageFilterType


class ImageFilterQuery(ObjectType):
    image_filters = NonNull(List(ImageFilterType))

    def resolve_image_filters(self, info):
        return ImageFilter.objects.all()
