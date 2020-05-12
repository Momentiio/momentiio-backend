import graphene
from django.db import models
from graphene import Field, List, Int, ID, NonNull, ObjectType
from graphene_django import DjangoObjectType
from user.graphql.types import ProfileType
from ..models import Post, Comment, Like
from .types import PostType, CommentType, LikeType
from friendship.models import Friend


class GetPostQuery(ObjectType):
    post = Field(PostType, post_id=ID())

    def resolve_post(self, info, post_id):
        post = Post.objects.get(id=post_id)
        return post


class GetPostCommentsQuery(ObjectType):
    post_comments = List(CommentType, post_id=ID(
    ), offset=Int(default_value=0), limit=Int(default_value=20))

    def resolve_post_comments(self, info, post_id, offset, limit):
        post = Post.objects.get(id=post_id)
        comments = Comment.objects.filter(post=post_id)
        return comments.distinct()[offset:offset+limit]


class GetPostLikesQuery(ObjectType):
    post_likes = List(LikeType, post_id=ID(
    ), offset=Int(default_value=0), limit=Int(default_value=20))

    def resolve_post_likes(self, info, post_id, offset, limit):
        post = Post.objects.get(id=post_id)
        likes = Like.objects.filter(post=post_id)
        return likes.distinct()[offset:offset+limit]


class PostsQuery(ObjectType):
    posts = NonNull(List(PostType))

    def resolve_posts(self, info):
        return Post.objects.all()


class FeedQuery(ObjectType):
    feed = List(PostType)

    def resolve_feed(self, info):
        friends = Friend.objects.friends(info.context.user)
        return Post.objects.filter(user__user__in=friends).order_by('-date_created')
