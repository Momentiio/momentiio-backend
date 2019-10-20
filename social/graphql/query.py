from django.db import models
from django.contrib.auth.models import User
import graphene
from .types import PostType
from ..models import Post


# class PostComment(DjangoObjectType):


# class PostLike(DjangoObjectType):


class PostsQuery(graphene.ObjectType):
    posts = graphene.NonNull(graphene.List(PostType))

    def resolve_posts(self, info):
        return Post.objects.all()
