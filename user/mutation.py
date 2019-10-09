from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.models import User
import graphene
from rest_framework.authtoken.models import Token
from graphene_django import DjangoObjectType

from friendship.models import Friend, Follow, Block, FriendshipRequest
from interests.models import Interest
from .models import Profile
from .query import ProfileType, ProfileUserType, UserType, FriendType, FriendshipRequestType


class LoginUser(graphene.Mutation):
    success = graphene.NonNull(graphene.Boolean)
    account = graphene.Field(UserType)
    token = graphene.String()
    message = graphene.String()

    class Arguments:
        username = graphene.NonNull(graphene.String)
        password = graphene.NonNull(graphene.String)

    @staticmethod
    def mutate(root, info, username, password):
        user = authenticate(username=username, password=password)
        if not user:
            return LoginUser(success=False, message="Invalid Credentials")
        login(info.context, user)
        token, _ = Token.objects.get_or_create(user=user)
        return LoginUser(success=True, account=user, token=token)


class LoginUserMutation(graphene.ObjectType):
    user_login = LoginUser.Field()


class LogoutUser(graphene.Mutation):
    success = graphene.NonNull(graphene.Boolean)

    class Arguments:
        pass

    @staticmethod
    def mutate(root, info):
        logout(info.context)
        return LogoutUser(success=True)


class LogoutUserMutation(graphene.ObjectType):
    logout_user = LogoutUser.Field()


class CreateUser(graphene.Mutation):
    user = graphene.Field(ProfileUserType)

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
    user = graphene.Field(ProfileUserType)
    errors = graphene.String()

    class Arguments:
        username = graphene.String(required=False)
        email = graphene.String(required=False)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)

    def mutate(self, info, username, email, first_name, last_name):
        try:
            user = info.context.user
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
        profile_avatar = graphene.String(required=False)
        bio = graphene.String(required=False)
        birth_date = graphene.types.datetime.Date(required=False)
        location = graphene.String(required=False)
        interests = graphene.List(graphene.ID, required=False)

    def mutate(self, info, profile_avatar, bio, location, birth_date, interests):
        try:
            user = info.context.user
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


class UpdatePrivacyPermission(graphene.Mutation):
    is_private = graphene.Boolean()
    errors = graphene.String()

    class Arguments:
        is_private = graphene.Boolean()

    def mutate(self, info, is_private):
        user = info.context.user
        if user:
            profile = user.profile
            profile.is_private = is_private
            profile.save()
            return UpdatePrivacyPermission(is_private=profile.is_private, errors=None)
        else:
            return UpdatePrivacyPermission(errors="User not found, please login or create an account")


class UpdatePrivacyMutation(graphene.ObjectType):
    update_privacy_status = UpdatePrivacyPermission.Field()


class UpdateHiddenPermission(graphene.Mutation):
    is_hidden = graphene.Boolean()
    errors = graphene.String()

    class Arguments:
        is_hidden = graphene.Boolean()

    def mutate(self, info, is_hidden):
        user = info.context.user
        if user:
            profile = user.profile
            profile.is_hidden = is_hidden
            profile.save()
            return UpdateHiddenPermission(is_hidden=profile.is_hidden, errors=None)
        else:
            return UpdateHiddenPermission(errors="User not found, please login or create an account")


class UpdateHiddenMutation(graphene.ObjectType):
    update_hidden_status = UpdateHiddenPermission.Field()

# Friendship Mutations


class RequestFriend(graphene.Mutation):
    errors = graphene.String()
    friendship_request = graphene.Field(FriendshipRequestType)

    class Arguments:
        to_user = graphene.ID()

    def mutate(self, info, to_user):
        try:
            from_user_id = info.context.user
            to_user_id = User.objects.get(pk=to_user)
        except User.DoesNotExist:
            return RequestFriend(errors="You must be logged in to send a friend request")

        if from_user_id and to_user_id:
            Friend.objects.add_friend(
                from_user_id,
                to_user_id,
                message=""
            )
        return RequestFriend(friendship_request=FriendshipRequest.objects.get(to_user=to_user_id), errors=None)


class RequestFriendMutation(graphene.ObjectType):
    request_friend = RequestFriend.Field()


class AddFriend(graphene.Mutation):
    new_friend = graphene.Field(FriendType)
    errors = graphene.String()

    class Arguments:
        to_user = graphene.ID()

    def mutate(self, info, to_user):
        requesting_user = info.context.user
        friend = User.objects.get(pk=to_user)
        is_private_or_hidden = friend.profile.is_private or friend.profile.is_hidden

        if not is_private_or_hidden:
            Friend.objects.create(
                from_user=requesting_user,
                to_user=friend,
            )
            new_friend = Friend.objects.get(
                to_user=friend, from_user=requesting_user)
            return AddFriend(new_friend=new_friend, errors=None)
        else:
            return AddFriend(errors="This user is private, You must send them a friend request to become friends.")


class AddFriendMutation(graphene.ObjectType):
    add_friend = AddFriend.Field()


class RemoveFriend(graphene.Mutation):
    friend_list = graphene.List(UserType)
    are_friends = graphene.Boolean()
    errors = graphene.String()

    class Arguments:
        to_user = graphene.ID()

    def mutate(self, info, to_user):
        requesting_user = info.context.user
        friend = User.objects.get(pk=to_user)
        are_friends = Friend.objects.are_friends(
            requesting_user, friend) == True

        if are_friends:
            Friend.objects.remove_friend(requesting_user, friend)
            friend_list = Friend.objects.friends(friend)
            are_friends = Friend.objects.are_friends(
                requesting_user, friend) == True
            return RemoveFriend(friend_list=friend_list, are_friends=are_friends)
        else:
            return RemoveFriend(errors="Cannot remove a Friendship that does not exist")


class RemoveFriendMutation(graphene.ObjectType):
    remove_friend = RemoveFriend.Field()


class AcceptFriendRequest(graphene.Mutation):
    new_friend = graphene.Field(FriendType)
    accepted = graphene.Boolean()
    errors = graphene.String()

    class Arguments:
        to_user = graphene.ID()

    def mutate(self, info, to_user):
        try:
            requesting_user = info.context.user
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
        to_user = graphene.ID()

    def mutate(self, info, to_user):
        try:
            from_friend = info.context.user
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
        to_user = graphene.ID()

    def mutate(self, info, to_user):
        try:
            requesting_user = info.context.user
            requested_friend = User.objects.get(pk=to_user)
            friend_request = FriendshipRequest.objects.get(
                to_user=requested_friend)

            friend_request.reject()
            return DeclineFriendRequest(friend_requests=Friend.objects.unrejected_requests(user=requesting_user), errors=None)

        except requested_friend.DoesNotExist:
            return DeclineFriendRequest(errors="user no longer exists")


class DeclineFriendRequestMutation(graphene.ObjectType):
    decline_friend_request = DeclineFriendRequest.Field()
