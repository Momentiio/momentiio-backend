from django.db import models
from django.contrib.auth.models import User
import graphene
from graphene import NonNull, ObjectType, List, Field, String, Union, ID
from graphene_django import DjangoObjectType
from address.models import Address, Country
from friendship.models import Friend, FriendshipRequest, Follow, Block
from social.models import Post
from social.query import PostType
from .models import Profile


class CountryType(DjangoObjectType):
    class Meta:
        model = Country
        only_fields = {
            "iso_code",
            "name"
        }


class AddressType(DjangoObjectType):
    class Meta:
        model = Address
        only_fields = {
            "address_line1",
            "address_line2",
            "postal_code",
            "city",
            "state_province",
            "country"
        }


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


class UserQuery(ObjectType):
    user = Field(ProfileUserType, user_id=ID())

    def resolve_user(self, info, user_id):
        return User.objects.get(id=user_id)


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
