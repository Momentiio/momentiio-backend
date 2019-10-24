from django.db.models import Q
from django.contrib.auth.models import User
import graphene
from graphene import NonNull, ObjectType, List, Field, String, Union, ID, Int
from graphene_django import DjangoObjectType
from address.graphql.types import AddressType
from friendship.models import Friend, FriendshipRequest, Follow, Block
from social.models import Post
from social.graphql.types import PostType
from .models import Profile


class FriendType(DjangoObjectType):
    class Meta:
        model = Friend


class FriendshipRequestType(DjangoObjectType):
    class Meta:
        model = FriendshipRequest


class FollowType(DjangoObjectType):
    class Meta:
        model = Follow


class UserType(DjangoObjectType):

    class Meta:
        model = User


class ProfileType(DjangoObjectType):
    user_name = String()
    full_name = String()
    address = Field(AddressType)
    posts = List(PostType)
    followers = List(UserType)
    following = List(UserType)

    class Meta:
        model = Profile
        only_fields = {
            "id",
            "user",
            "profile_avatar",
            "bio",
            "location",
            "birth_date",
            "interests",
            "is_private",
            "is_hidden"
        }

    def resolve_user_name(self, info):
        return self.user.username

    def resolve_full_name(self, info):
        return self.user.full_name

    def resolve_address(self, info):
        return self.user.address

    def resolve_posts(self, info):
        return Post.objects.filter(user=self.id)

    def resolve_followers(self, info):
        request_user = User.objects.get(pk=self.user.id)
        return Follow.objects.followers(request_user)

    def resolve_following(self, info):
        request_user = User.objects.get(pk=self.user.id)
        return Follow.objects.following(request_user)


class ProfileUserType(DjangoObjectType):
    address = Field(AddressType)
    profile = Field(ProfileType)
    friends = List(UserType)
    friend_requests = List(FriendshipRequestType)
    friend_request_count = String()

    class Meta:
        model = User
        only_fields = {
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
        }

    def resolve_friends(self, info):
        return Friend.objects.friends(user=self)

    def resolve_friend_requests(self, info):
        return Friend.objects.unrejected_requests(user=self)

    def resolve_friend_request_count(self, info):
        return Friend.objects.unrejected_request_count(user=self)


class UserListQuery(ObjectType):
    users = NonNull(List(ProfileType))

    def resolve_users(self, info):
        return Profile.objects.all()


class GetUserQuery(ObjectType):
    user = Field(ProfileUserType, user_id=ID())

    def resolve_user(self, info, user_id):
        return User.objects.get(id=user_id)


class UserSearchQuery(graphene.ObjectType):
    user_search = graphene.List(ProfileUserType, search=graphene.String(
    ), offset=Int(default_value=0), limit=Int(default_value=20))

    def resolve_user_search(self, info, offset, limit, search=None, ** kwargs):
        if search:
            return User.objects.filter(
                Q(username__icontains=search)
            ).exclude(Q(profile__is_hidden=True)).distinct()[offset:offset+limit]

        return User.objects.all().exclude(Q(profile__is_hidden=True)).distinct()[offset:offset+limit]


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
