import graphene
from django.db.models import Q
from django.contrib.auth.models import User
from graphene import NonNull, ObjectType, List, Field, String, Union, ID, Int
from graphene_django import DjangoObjectType
from friendship.models import Friend, FriendshipRequest, Follow, Block

from address.graphql.types import AddressType
from social.models import Post
from social.graphql.types import PostType, FriendType, FriendshipRequestType, FollowType
from .types import UserType, ProfileType, FullUserType
from ..models import Profile


class UserAuth(ObjectType):
    me = Field(User)
    users = List(User)

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication Failure!')
        return user


class UserSearchQuery(graphene.ObjectType):
    user_search = graphene.List(FullUserType, search=graphene.String(
    ), offset=Int(default_value=0), limit=Int(default_value=20))

    def resolve_user_search(self, info, offset, limit, search=None, ** kwargs):
        if search:
            return User.objects.filter(
                Q(username__icontains=search)
            ).exclude(Q(profile__is_hidden=True)).distinct()[offset:offset+limit]

        return User.objects.all().exclude(Q(profile__is_hidden=True)).distinct()[offset:offset+limit]


class GetUserQuery(ObjectType):
    look_up_user = Field(ProfileType, user_id=ID())

    def resolve_look_up_user(self, info, user_id):
        profile = User.objects.get(id=user_id).profile
        return profile


class GetAuthUserProfileQuery(ObjectType):
    user_profile = Field(FullUserType)

    def resolve_user_profile(self, info):
        profile = info.context.user
        return profile
