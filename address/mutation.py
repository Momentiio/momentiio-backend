from django.contrib.auth.models import User
import graphene
from graphene_django import DjangoObjectType
from .models import Address
from user.query import ProfileUserType, CountryType, AddressType


class UpdateAddress(graphene.Mutation):
    address = graphene.Field(AddressType)
    errors = graphene.String()

    class Arguments:
        address_line1 = graphene.String()
        address_line2 = graphene.String()
        postal_code = graphene.String()
        city = graphene.String()
        state_province = graphene.String()
        # country = graphene.String()

    def mutate(self, info, address_line1, address_line2, city, state_province, postal_code):
        user = info.context.user
        address = user.address

        if address_line1 is not None:
            address.address_line1 = address_line1
        if address_line2 is not None:
            address.address_line2 = address_line2
        if city is not None:
            address.city = city
        if state_province is not None:
            address.state_province = state_province
        if postal_code is not None:
            address.postal_code = postal_code
        # if country is not None:
        #     address.country = country
        address.save()
        return UpdateAddress(address=address, errors=None)


class UpdateAddressMutation(graphene.ObjectType):
    update_address = UpdateAddress.Field()
