from django.db import models
from django.contrib.auth.models import User
import graphene
from graphene import NonNull, ObjectType, List, Field, String, Union
from graphene_django import DjangoObjectType
from . import models


class CommentType(DjangoObjectType):
    class Meta:
        model = models.Comment
        only_fields = [
            "user",
            "photo",
            "content",
            "date_created"
        ]


class PostType(DjangoObjectType):
    comments = List(CommentType)

    class Meta:
        model = models.Post
        only_fields = [
            "id",
            "user",
            "caption",
            "photo",
            "date_created",
            "date_updated"
        ]

    def resolve_comments(self, info):
        return self.comments.objects.all()


# class PostComment(DjangoObjectType):


# class PostLike(DjangoObjectType):


class PostsQuery(ObjectType):
    posts = NonNull(List(PostType))

    def resolve_posts(self, info):
        return models.Post.objects.all()
