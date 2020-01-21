import graphene
from graphene_django import DjangoObjectType
from address.models import Address


class CountryType(graphene.ObjectType):
    code = graphene.NonNull(graphene.String)
    name = graphene.NonNull(graphene.String)

    def resolve_code(dict, info):
        return dict["code"]

    def resolve_name(dict, info):
        return dict["name"]


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
