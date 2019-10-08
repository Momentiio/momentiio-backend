from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import graphene
import graphql_jwt
from graphene_django import DjangoObjectType

from friendship.models import Friend, Follow, Block, FriendshipRequest
from interests.models import Interest
from .models import Profile
from .query import ProfileType, UserType, FriendType, FriendshipRequestType


class UserAuth(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class CreateUserMutation(graphene.ObjectType):
    create_user = CreateUser.Field()

# class UploadImageMutation(graphene.ClientIdMutation):
#     class Input:
#         pass
#     success = graphene.String()
#     @classmethod
#     def mutate_and_get_payload(cls, root, info, **input):
#         files = info.context.FILES
#         return UploadFile(success=True)


class InterestType(DjangoObjectType):
    class Meta:
        model = Interest


class UpdateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    errors = graphene.String()

    class Arguments:
        user_id = graphene.ID(required=True)
        username = graphene.String(required=False)
        email = graphene.String(required=False)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)

    def mutate(self, info, user_id, username, email, first_name, last_name):
        try:
            _id = int(user_id)
            user = User.objects.get(id=_id)
        except User.DoesNotExist:
            return UpdateUser(errors='User could not be found')
        if username is not None:
            user.username = username
        if email is not None:
            user.email = email
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        user.save()
        return UpdateUser(user=user, errors=None)


class UpdateUserMutation(graphene.ObjectType):
    update_user = UpdateUser.Field()


class UpdateUserProfile(graphene.Mutation):
    errors = graphene.String()
    profile = graphene.Field(ProfileType)

    class Arguments:
        user_id = graphene.ID()
        profile_avatar = graphene.String()
        bio = graphene.String()
        birth_date = graphene.types.datetime.Date()
        location = graphene.String()
        interests = graphene.List(graphene.ID)

    def mutate(self, info, user_id, profile_avatar, bio, location, birth_date, interests):
        try:
            _id = int(user_id)
            user = User.objects.get(id=_id)
        except User.DoesNotExist:
            return UpdateUserProfile(errors='Please Login')
        profile = user.profile
        if profile_avatar is not None:
            profile.profile_avatar = profile_avatar
        if bio is not None:
            profile.bio = bio
        if location is not None:
            profile.location = location
        if birth_date is not None:
            profile.birth_date = birth_date
        if interests is not None:
            profile.interests = interests

        profile.save()

        return UpdateUserProfile(profile=profile, errors=None)


class UpdateUserProfileMutation(graphene.ObjectType):
    update_profile = UpdateUserProfile.Field()


class RequestFriend(graphene.Mutation):
    errors = graphene.String()
    friendship_request = graphene.Field(FriendshipRequestType)

    class Arguments:
        from_user = graphene.ID()
        to_user = graphene.ID()
        message = graphene.String(required=False)

    def mutate(self, info, from_user, to_user, message):
        try:
            from_user_id = User.objects.get(pk=from_user)
            to_user_id = User.objects.get(pk=to_user)
        except User.DoesNotExist:
            return RequestFriend(errors="You must be logged in to send a friend request")

        if from_user_id and to_user_id:
            Friend.objects.add_friend(
                from_user_id,
                to_user_id,
                message=message
            )
        return RequestFriend(friendship_request=FriendshipRequest.objects.get(to_user=to_user_id), errors=None)


class RequestFriendMutation(graphene.ObjectType):
    request_friend = RequestFriend.Field()


class AddFriend(graphene.Mutation):
    new_friend = graphene.Field(FriendType)

    class Arguments:
        from_user = graphene.ID()
        to_user = graphene.ID()

    def mutate(self, info, from_user, to_user):
        requesting_user = User.objects.get(pk=from_user)
        friend = User.objects.get(pk=to_user)

        Friend.objects.create(
            from_user=requesting_user,
            to_user=friend,
        )
        new_friend = Friend.objects.get(
            to_user=friend, from_user=requesting_user)
        return AddFriend(new_friend=new_friend)


class AddFriendMutation(graphene.ObjectType):
    add_friend = AddFriend.Field()


class AcceptFriendRequest(graphene.Mutation):
    new_friend = graphene.Field(FriendType)
    accepted = graphene.Boolean()
    errors = graphene.String()

    class Arguments:
        from_user = graphene.ID()
        to_user = graphene.ID()

    def mutate(self, info, from_user, to_user):
        try:
            requesting_user = User.objects.get(pk=from_user)
            requested_friend = User.objects.get(pk=to_user)
            friend_request = FriendshipRequest.objects.get(
                to_user=requested_friend)
            friend_request.accept()
            new_friend = Friend.objects.get(
                to_user=requested_friend, from_user=requesting_user)
            accepted = Friend.objects.are_friends(
                requesting_user, requested_friend) == True

            return AcceptFriendRequest(
                new_friend=new_friend, accepted=accepted, errors=None)

        except requested_friend.DoesNotExist:
            return AcceptFriendRequest(errors="user no longer exists")


class AcceptFriendRequestMutation(graphene.ObjectType):
    accept_friend_request = AcceptFriendRequest.Field()


class CancelFriendRequest(graphene.Mutation):
    friend_requests = graphene.List(FriendshipRequestType)

    class Arguments:
        from_user = graphene.ID()
        to_user = graphene.ID()

    def mutate(self, info, from_user, to_user):
        try:
            from_friend = User.objects.get(pk=from_user)
            to_friend = User.objects.get(pk=to_user)
        except from_friend.DoesNotExist or to_friend.DoesNotExist:
            return CancelFriendRequest(friend_requests=Friend.objects.unrejected_requests(user=from_friend))
        if from_friend and to_friend:
            request_to_cancel = FriendshipRequest.objects.get(
                to_user=to_friend)
            request_to_cancel.cancel()
            return CancelFriendRequest(friend_requests=Friend.objects.unrejected_requests(user=from_friend))


class CancelFriendRequestMutation(graphene.ObjectType):
    cancel_friend_request = CancelFriendRequest.Field()


class DeclineFriendRequest(graphene.Mutation):
    friend_requests = graphene.List(FriendshipRequestType)
    errors = graphene.String()

    class Arguments:
        from_user = graphene.ID()
        to_user = graphene.ID()

    def mutate(self, info, from_user, to_user):
        try:
            requesting_user = User.objects.get(pk=from_user)
            requested_friend = User.objects.get(pk=to_user)
            friend_request = FriendshipRequest.objects.get(
                to_user=requested_friend)

            friend_request.reject()
            return DeclineFriendRequest(friend_requests=Friend.objects.unrejected_requests(user=requesting_user), errors=None)

        except requested_friend.DoesNotExist:
            return DeclineFriendRequest(errors="user no longer exists")


class DeclineFriendRequestMutation(graphene.ObjectType):
    decline_friend_request = DeclineFriendRequest.Field()
