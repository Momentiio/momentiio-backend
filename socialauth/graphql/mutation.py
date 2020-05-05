import os
from django.contrib.auth import get_user_model

import graphene
import graphene_django
from graphene import Field, String
from graphene_django import DjangoObjectType
import graphql_social_auth

from user.graphql.types import UserType


class SocialAuthMutation(graphql_social_auth.SocialAuthMutation):
    user = Field(UserType)

    @classmethod
    def resolve(cls, root, info, social, **kwargs):
        return cls(user=social.user)
