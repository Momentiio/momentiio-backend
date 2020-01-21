from django.contrib.auth.models import User
import graphene
from graphene_django import DjangoObjectType
from django_countries.fields import CountryField
from ..models import Address
from .types import CountryType, AddressType


class UpdateAddress(graphene.Mutation):
    address = graphene.Field(AddressType)
    errors = graphene.String()

    class Arguments:
        address_line1 = graphene.String()
        address_line2 = graphene.String()
        postal_code = graphene.String()
        city = graphene.String()
        state_province = graphene.String()
        country = graphene.String()

    def mutate(self, info, address_line1, address_line2, city, state_province, postal_code, country):
        address, _ = Address.objects.update_or_create(
            user=info.context.user,
            defaults={
                'address_line1': address_line1,
                'address_line2': address_line2,
                'postal_code': postal_code,
                'city': city,
                'state_province': state_province,
                'country': country
            }
        )
        address.save()
        return UpdateAddress(address=address, errors=None)


class UpdateAddressMutation(graphene.ObjectType):
    update_address = UpdateAddress.Field()
