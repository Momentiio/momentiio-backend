import graphene
from django.contrib.auth import get_user_model
from graphene import Field, List, String
from graphene_django import DjangoObjectType
from friendship.models import Follow, Friend

from address.graphql.types import AddressType
from invites.graphql.types import InviteType
from social.graphql.types import PostType, FriendshipRequestType
from social.models import Post
from ..models import Profile


class UserType(DjangoObjectType):
    profile_avatar = String()
    location = String()

    class Meta:
        model = get_user_model()
        only_fields = {
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "dateJoined",
            "is_hidden",
            "is_private",
        }

    def resolve_profile_avatar(self, info):
        return self.profile.profile_avatar

    def resolve_location(self, info):
        return self.profile.location


class ProfileType(DjangoObjectType):
    username = String()
    full_name = String()
    address = Field(AddressType)
    posts = List(PostType)
    followers = List(UserType)
    following = List(UserType)

    class Meta:
        model = Profile
        only_fields = {
            "id",
            "profile_avatar",
            "location",
            "bio",
            "birth_date",
            "interests",
        }

    def resolve_username(self, info):
        return self.user.username

    def resolve_full_name(self, info):
        return self.user.full_name

    def resolve_address(self, info):
        return self.user.address

    def resolve_posts(self, info):
        return Post.objects.filter(user=self.id)

    def resolve_followers(self, info):
        request_user = get_user_model().objects.get(pk=self.user.id)
        return Follow.objects.followers(request_user)

    def resolve_following(self, info):
        request_user = get_user_model().objects.get(pk=self.user.id)
        return Follow.objects.following(request_user)


class AuthUserType(DjangoObjectType):
    profileAvatar = String()
    address = Field(AddressType)
    friends = List(UserType)
    friend_requests = List(FriendshipRequestType)
    friend_request_count = String()

    class Meta:
        model = get_user_model()
        only_fields = {
            "id",
            "username",
            "first_name",
            "last_name",
            "type",
            "phone_number",
            "email",
            "is_active",
            "sponsor",
            "date_joined",
            "is_hidden",
            "is_private",
            "invites"
        }

    def resolve_profile_avatar(self, info):
        return self.user.profile.profile_avatar

    def resolve_friends(self, info):
        return Friend.objects.friends(user=self)

    def resolve_friend_requests(self, info):
        return Friend.objects.unrejected_requests(user=self)

    def resolve_friend_request_count(self, info):
        return Friend.objects.unrejected_request_count(user=self)
