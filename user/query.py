from django.db import models
from django.contrib.auth.models import models
import graphene
from graphene import NonNull, ObjectType, List, Field, String, Union, ID
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
    user_name = String()
    full_name = String()

    class Meta:
        model = models.Profile
        only_fields = {
            "id",
            "user",
            "profile_avatar",
            "bio",
            "location",
            "birth_date",
            "interests",
            "address"
        }

    def resolve_user_name(self, info):
        return self.user.username

    def resolve_full_name(self, info):
        return self.user.full_name


class UserListQuery(ObjectType):
    users = NonNull(List(ProfileType))

    def resolve_users(self, info):
        return models.Profile.objects.all()


class UserQuery(ObjectType):
    user = Field(ProfileType, user_id=ID())

    def resolve_user(self, info, user_id):
        return models.Profile.objects.get(pk=user_id)


class UserAuth(ObjectType):
    me = graphene.Field(User)
    users = graphene.List(User)

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication Failure!')
        return user
