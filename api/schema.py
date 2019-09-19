from django.db import models
import graphene
from graphene import List, Schema, ObjectType, NonNull, ID
from graphene_django import DjangoObjectType
from social.query import PostsQuery


class Query(
    PostsQuery,
):
    pass


schema = Schema(query=Query)
