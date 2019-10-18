from django.db import models
import graphene
from graphene_django import DjangoObjectType
from ..models import Post, Comment, Like


class LikeType(DjangoObjectType):
    class Meta:
        model = Like


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        only_fields = [
            "user",
            "photo",
            "content",
            "date_created"
        ]


class PostType(DjangoObjectType):
    comments = graphene.List(CommentType)
    likes = graphene.List(LikeType)

    class Meta:
        model = Post
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

    def resolve_likes(self, info):
        return self.likes.objects.all()
