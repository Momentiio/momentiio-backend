from django.db import models
import graphene
from graphene import List, Schema, ObjectType, NonNull, ID
from graphene_django import DjangoObjectType
from social.query import PostsQuery
from user.query import UserListQuery, UserQuery


class Query(
    PostsQuery,
    UserListQuery,
    UserQuery
):
    pass


schema = Schema(query=Query)
