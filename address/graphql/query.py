from graphene import Field, NonNull, List, Enum, ID, ObjectType, String
from graphene_django import DjangoObjectType
from django_countries import countries
from .types import CountryType, AddressType

from ..models import Address


class AddressQuery(DjangoObjectType):
    class Meta:
        model = Address


class CountryQuery(object):
    countries = NonNull(List(NonNull(CountryType)))

    def resolve_countries(root, info):
        return [{"code": key, "name": value} for key, value in dict(countries).items()]


class GetAddressByID(ObjectType):
    address_by_id = Field(AddressType, id=ID())

    def resolve_address_by_id(self, info, id):
        address = Address.objects.get(id=id)
        if address is not None:
            return address
        else:
            raise Exception('No address could be found')
