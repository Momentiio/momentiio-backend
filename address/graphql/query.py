from graphene import Field, NonNull, List, Enum, ID, ObjectType, String
from graphene_django import DjangoObjectType
from django_countries import countries
from .types import CountryType

from ..models import Address


class Address(DjangoObjectType):
    class Meta:
        model = Address


class CountryQuery(object):
    countries = NonNull(List(NonNull(CountryType)))

    def resolve_countries(root, info):
        return [{"code": key, "name": value} for key, value in dict(countries).items()]
