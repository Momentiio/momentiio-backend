from django.db import models
import graphene
from graphene import List, Schema, ObjectType, NonNull, ID
from graphene_django import DjangoObjectType
from social.query import PostsQuery
from user.query import UsersQuery


class Query(
    PostsQuery,
    UsersQuery
):
    pass


schema = Schema(query=Query)
