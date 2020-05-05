from django.contrib.auth import get_user_model

import graphene
import graphene_django
from graphene_django import DjangoObjectType
from user.graphql.types import UserType


class SocialAuthUserQuery(graphene.ObjectType):
    users = graphene.List(UserType)
