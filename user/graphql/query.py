import graphene
from django.db.models import Q
from django.contrib.auth import get_user_model
from graphene import NonNull, ObjectType, List, Field, String, Union, ID, Int
from graphene_django import DjangoObjectType
from friendship.models import Friend, FriendshipRequest, Follow, Block

from address.graphql.types import AddressType
from social.models import Post
from social.graphql.types import PostType, FriendType, FriendshipRequestType, FollowType
from .types import UserType, ProfileType, AuthUserType
from ..models import Profile


class UserAuth(ObjectType):
    me = Field(get_user_model())
    users = List(get_user_model())

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication Failure!')
        return user


class UserSearchQuery(graphene.ObjectType):
    user_search = graphene.List(AuthUserType, search=graphene.String(
    ), offset=Int(default_value=0), limit=Int(default_value=20))

    def resolve_user_search(self, info, offset, limit, search=None, ** kwargs):
        if search:
            return get_user_model().objects.filter(
                Q(username__icontains=search)
            ).exclude(Q(profile__is_hidden=True)).distinct()[offset:offset+limit]

        return get_user_model().objects.all().exclude(Q(profile__is_hidden=True)).distinct()[offset:offset+limit]


class GetUserQuery(ObjectType):
    look_up_user = Field(ProfileType, user_id=ID())

    def resolve_look_up_user(self, info, user_id):
        profile = get_user_model().objects.get(id=user_id).profile
        return profile


class GetAuthUserProfileQuery(ObjectType):
    user_profile = Field(AuthUserType)

    def resolve_user_profile(self, info):
        profile = info.context.user
        return profile
