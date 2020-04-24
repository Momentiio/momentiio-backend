import graphene
from django.contrib.auth import get_user_model
from graphene import Field, List, String
from graphene_django import DjangoObjectType
from friendship.models import Follow, Friend


from address.graphql.types import AddressType
from address.models import Address
from invites.graphql.types import InviteType
from social.graphql.types import PostType, FriendshipRequestType
from social.models import Post
from ..models import Profile


class UserType(DjangoObjectType):
    profile_avatar = String()
    address = Field(AddressType)
    location = String()
    incoming_friend_requests = List(FriendshipRequestType)
    outgoing_friend_requests = List(FriendshipRequestType)
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

    def resolve_address(self, info):
        return Address.objects.get(user=self)

    def resolve_profile_avatar(self, info):
        if self.profile.profile_avatar:
            return self.profile.profile_avatar.url
        else:
            return self.profile.profile_avatar

    def resolve_location(self, info):
        return self.profile.location

    def resolve_incoming_friend_requests(self, info):
        return Friend.objects.unrejected_requests(user=self)

    def resolve_outgoing_friend_requests(self, info):
        return Friend.objects.sent_requests(user=self)

    def resolve_friend_request_count(self, info):
        return Friend.objects.unrejected_request_count(user=self)


class ProfileType(DjangoObjectType):
    user_id = String()
    username = String()
    full_name = String()
    posts = List(PostType)
    followers = List(UserType)
    following = List(UserType)

    class Meta:
        model = Profile
        only_fields = {
            'id',
            'bio',
            'location',
            'birth_date',
            'interests',
            'profile_avatar'
        }

    def resolve_user_id(self, info):
        return self.user.id

    def resolve_username(self, info):
        return self.user.username

    def resolve_full_name(self, info):
        return self.user.full_name

    def resolve_posts(self, info):
        return Post.objects.filter(user=self.id)

    def resolve_followers(self, info):
        user = self.user
        return Follow.objects.followers(user)

    def resolve_following(self, info):
        user = self.user
        return Follow.objects.following(user)
