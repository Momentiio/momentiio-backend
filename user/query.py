from django.db import models
from django.contrib.auth.models import models
import graphene
from graphene import NonNull, ObjectType, List, Field, String, Union
from graphene_django import DjangoObjectType
from address.models import Country
from . import models


class CountryType(DjangoObjectType):
    class Meta:
        model = Country
        only_fields = {
            "iso_code",
            "name"
        }


class UserAddress(DjangoObjectType):
    class Meta:
        model = models.Address
        only_fields = {
            "address_line1",
            "address_line2",
            "postal_code",
            "city",
            "state_province",
            "country"
        }


class User(DjangoObjectType):
    class Meta:
        model = models.User
        only_fields = {
            "id",
            "username",
            "first_name",
            "last_name"
        }


class ProfileType(DjangoObjectType):

    class Meta:
        model = models.Profile
        only_fields = {
            "user",
            "profile_avatar",
            "bio",
            "location",
            "birth_date",
            "interests",
            "address"
        }


class UsersQuery(ObjectType):
    users = NonNull(List(ProfileType))

    def resolve_users(self, info):
        return models.Profile.objects.all()
