from django.db import models
from django.contrib.auth.models import User
import datetime
import graphene
from graphene_django import DjangoObjectType
from .types import PostType, LikeType, CommentType
from ..models import Post, Comment, Like


class AddPost(graphene.Mutation):
    post = graphene.Field(PostType)
    errors = graphene.String()

    class Arguments:
        photo = graphene.String()
        caption = graphene.String()

    def mutate(self, info, photo, caption):
        user = info.context.user.profile
        if not user:
            return AddPost(errors="You must be logged in to create a post")
        post = Post.objects.create(
            user=user,
            photo=photo,
            caption=caption,
            date_created=datetime.datetime.now()
        )
        return AddPost(post=post, errors=None)


class AddPostMutation(graphene.ObjectType):
    add_post = AddPost.Field()
