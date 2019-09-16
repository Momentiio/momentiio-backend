from wagtail.core.fields import StreamField
from graphene.types import Scalar

from graphene_django.converter import convert_django_field
from wagtail.images.models import Image
from wagtail.embeds.models import Embed
from graphene_django import DjangoObjectType


class GenericStreamFieldType(Scalar):
    @staticmethod
    def serialize(stream_value):
        return stream_value.stream_data


@convert_django_field.register(StreamField)
def convert_stream_field(field, registry=None):
    return GenericStreamFieldType(
        description=field.help_text, required=not field.null
    )


class WagtailImageNode(DjangoObjectType):
    class Meta:
        model = Image
        exclude_fields = ['tags']

@convert_django_field.register(Image)
def convert_image(field, registry=None):
    return WagtailImageNode(
        description=field.help_text, required=not field.null
    )


class WagtailEmbedNode(DjangoObjectType):
    class Meta:
        model = Embed

        
@convert_django_field.register(Embed)
def convert_embed(field, registry=None):
    return WagtailEmbedNode(
        description=field.help_text, required=not field.null
    )