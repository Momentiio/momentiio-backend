import graphene
from graphene_django import DjangoObjectType
from address.models import Address, Country


class CountryType(DjangoObjectType):
    class Meta:
        model = Country
        only_fields = {
            "iso_code",
            "name"
        }


class AddressType(DjangoObjectType):
    class Meta:
        model = Address
        only_fields = {
            "address_line1",
            "address_line2",
            "postal_code",
            "city",
            "state_province",
            "country"
        }
