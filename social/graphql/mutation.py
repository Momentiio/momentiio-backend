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


class UpdatePost(graphene.Mutation):
    post = graphene.Field(PostType)
    updated_on = graphene.String()
    errors = graphene.String()

    class Arguments:
        post_id = graphene.ID()
        photo = graphene.String(required=False)
        caption = graphene.String(required=False)

    def mutate(self, info, post_id, photo, caption):
        post = Post.objects.get(id=post_id)
        if photo is not None:
            post.photo = photo
        else:
            post.photo = post.photo
        if caption is not None:
            post.caption = caption
        else:
            post.caption = post.caption
        _updated = post.date_updated = datetime.datetime.now()
        post.save()
        return UpdatePost(post=post, updated_on=_updated)


class UpdatePostMutation(graphene.ObjectType):
    update_post = UpdatePost.Field()


class DeletePost(graphene.Mutation):
    deleted = graphene.Boolean()

    class Arguments:
        post_id = graphene.ID()

    def mutate(self, info, post_id):
        post = Post.objects.get(id=post_id)
        post.delete()
        return DeletePost(deleted=True)


class DeletePostMutation(graphene.ObjectType):
    delete_post = DeletePost.Field()
