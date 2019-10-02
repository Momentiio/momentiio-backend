from django.db import models
from django.contrib.auth.models import User
import graphene
from graphene import NonNull, ObjectType, List, Field, String, Union
from graphene_django import DjangoObjectType
from . import models
from user.query import UserType


class Post(DjangoObjectType):
    class Meta:
        model = models.Post
        only_fields = [
            "user",
            "caption",
            "photo",
            "date_created",
            "date_updated"
        ]


# class PostComment(DjangoObjectType):


# class PostLike(DjangoObjectType):


class PostsQuery(ObjectType):
    posts = NonNull(List(Post))

    def resolve_posts(self, info):
        return models.Post.objects.all()
