from django.db import models
import datetime
import graphene
from graphene import Field, List, String, ID, Boolean, ObjectType, Mutation
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
from system.graphql.mutation import create_system_image
from system.graphql.types import ImageType
from .types import PostType, LikeType, CommentType
from ..models import Post, Comment, Like


class CreatePost(Mutation):
    post = Field(PostType)
    errors = String()

    class Arguments:
        caption = String()
        post_media = Upload(required=True)

    def mutate(self, info, caption, post_media):
        user = info.context.user.profile
        if not user:
            return CreatePost(errors="You must be logged in to create a post")

        post = Post.objects.create(
            user=user,
            caption=caption,
            date_created=datetime.datetime.now()
        )

        for file in post_media:
            image = create_system_image(info, file, post.id)

        post.save()
        return CreatePost(post=post, errors=None)


class CreatePostMutation(ObjectType):
    create_post = CreatePost.Field()


class UpdatePost(Mutation):
    post = Field(PostType)
    updated_on = String()
    errors = String()

    class Arguments:
        post_id = ID()
        caption = String(required=False)

    def mutate(self, info, post_id, caption):
        post = Post.objects.get(id=post_id)
        if caption:
            post.caption = caption
        else:
            post.caption = post.caption
        _updated = post.date_updated = datetime.datetime.now()
        post.save()
        return UpdatePost(post=post, updated_on=_updated)


class UpdatePostMutation(ObjectType):
    update_post = UpdatePost.Field()


class DeletePost(Mutation):
    deleted = Boolean()

    class Arguments:
        post_id = ID()

    def mutate(self, info, post_id):
        post = Post.objects.get(id=post_id)
        post.delete()
        return DeletePost(deleted=True)


class DeletePostMutation(ObjectType):
    delete_post = DeletePost.Field()


class LikePost(Mutation):
    like = Field(LikeType)
    errors = String()

    class Arguments:
        post_id = ID()

    def mutate(self, info, post_id):
        like = Like.objects.create(
            user=info.context.user.profile,
            post=Post.objects.get(id=post_id),
            date_created=datetime.datetime.now()
        )
        return LikePost(like=like, errors=None)


class LikePostMutation(ObjectType):
    like_post = LikePost.Field()


class RemoveLikePost(Mutation):
    removed = Boolean()
    errors = String()

    class Arguments:
        like_id = ID()

    def mutate(self, info, like_id):
        like = Like.objects.get(id=like_id)
        like.delete()
        return RemoveLikePost(removed=True, errors=None)


class RemoveLikePostMutation(ObjectType):
    remove_like = RemoveLikePost.Field()


class AddPostComment(Mutation):
    comment = Field(CommentType)
    errors = String()

    class Arguments:
        post_id = ID()
        comment = String()

    def mutate(self, info, post_id, comment):
        comment = Comment.objects.create(
            user=info.context.user.profile,
            post=Post.objects.get(id=post_id),
            comment=comment,
            date_created=datetime.datetime.now()
        )
        return AddPostComment(comment=comment, errors=None)


class AddPostCommentMutation(ObjectType):
    add_comment = AddPostComment.Field()


class UpdatePostComment(Mutation):
    comment = Field(CommentType)
    errors = String()

    class Arguments:
        comment_id = ID()
        comment = String()

    def mutate(self, info, comment_id, comment):
        comment = Comment.objects.get(id=comment_id)
        if not comment:
            return UpdatePostComment(errors="Looks like this comment has been deleted")
        else:
            comment.comment = comment
            comment.save()
            return UpdatePostComment(comment=comment, errors=None)


class UpdatePostCommentMutation(ObjectType):
    update_comment = UpdatePostComment.Field()


class DeletePostComment(Mutation):
    deleted = Boolean()
    errors = String()

    class Arguments:
        comment_id = ID()

    def mutate(self, info, comment_id):
        user = info.context.user
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return DeletePostComment(deleted=True, errors=None)


class DeletePostCommentMutation(ObjectType):
    delete_comment = DeletePostComment.Field()
