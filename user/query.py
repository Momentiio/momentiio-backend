from django.db import models
from django.contrib.auth.models import models
import graphene
from graphene import NonNull, ObjectType, List, Field, String, Union
from graphene_django import DjangoObjectType
from . import models


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
            "bio",
            "location",
            "birth_date",
            "interests",
            "postal_address"
        }


class UsersQuery(ObjectType):
    users = NonNull(List(ProfileType))

    def resolve_users(self, info):
        return models.Profile.objects.all()
