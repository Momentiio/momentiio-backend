from django.db import models
import datetime
import graphene
from graphene_django import DjangoObjectType
from system.graphql.mutation import create_system_image
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
        post_image = create_system_image(info, photo)
        post = Post.objects.create(
            user=user,
            photo=post_image.image,
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
        if photo:
            post_image = create_system_image(info, photo)
            post.photo = post_image
        else:
            post.photo = post.photo
        if caption:
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


class LikePost(graphene.Mutation):
    like = graphene.Field(LikeType)
    errors = graphene.String()

    class Arguments:
        post_id = graphene.ID()

    def mutate(self, info, post_id):
        like = Like.objects.create(
            user=info.context.user.profile,
            post=Post.objects.get(id=post_id),
            date_created=datetime.datetime.now()
        )
        return LikePost(like=like, errors=None)


class LikePostMutation(graphene.ObjectType):
    like_post = LikePost.Field()


class RemoveLikePost(graphene.Mutation):
    removed = graphene.Boolean()
    errors = graphene.String()

    class Arguments:
        like_id = graphene.ID()

    def mutate(self, info, like_id):
        like = Like.objects.get(id=like_id)
        like.delete()
        return RemoveLikePost(removed=True, errors=None)


class RemoveLikePostMutation(graphene.ObjectType):
    remove_like = RemoveLikePost.Field()


class AddPostComment(graphene.Mutation):
    comment = graphene.Field(CommentType)
    errors = graphene.String()

    class Arguments:
        post_id = graphene.ID()
        content = graphene.String()

    def mutate(self, info, post_id, content):
        comment = Comment.objects.create(
            user=info.context.user.profile,
            post=Post.objects.get(id=post_id),
            content=content,
            date_created=datetime.datetime.now()
        )
        return AddPostComment(comment=comment, errors=None)


class AddPostCommentMutation(graphene.ObjectType):
    add_comment = AddPostComment.Field()


class UpdatePostComment(graphene.Mutation):
    comment = graphene.Field(CommentType)
    errors = graphene.String()

    class Arguments:
        comment_id = graphene.ID()
        content = graphene.String()

    def mutate(self, info, comment_id, content):
        comment = Comment.objects.get(id=comment_id)
        if not comment:
            return UpdatePostComment(errors="Looks like this comment has been deleted")
        else:
            comment.content = content
            comment.save()
            return UpdatePostComment(comment=comment, errors=None)


class UpdatePostCommentMutation(graphene.ObjectType):
    update_comment = UpdatePostComment.Field()


class DeletePostComment(graphene.Mutation):
    deleted = graphene.Boolean()
    errors = graphene.String()

    class Arguments:
        comment_id = graphene.ID()

    def mutate(self, info, comment_id):
        user = info.context.user
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return DeletePostComment(deleted=True, errors=None)


class DeletePostCommentMutation(graphene.ObjectType):
    delete_comment = DeletePostComment.Field()
