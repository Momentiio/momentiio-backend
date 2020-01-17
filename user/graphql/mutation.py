from django.contrib.auth import get_user_model, authenticate, login, logout
import graphene
from rest_framework.authtoken.models import Token
from graphql import GraphQLError
from graphene_django import DjangoObjectType

from friendship.models import Friend, Follow, Block, FriendshipRequest
from interests.models import Interest
from interests.graphql.types import InterestType
from social.graphql.types import FriendType, FriendshipRequestType
from system.graphql.types import ImageType
from system.graphql.mutation import create_system_image
from .types import UserType, ProfileType
from ..models import Profile


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
    user_logout = LogoutUser.Field()


class LookUpUsername(graphene.Mutation):
    is_taken = graphene.Boolean()

    class Arguments:
        username = graphene.String(required=True)

    def mutate(self, info, username):
        is_taken = get_user_model().objects.filter(username=username)
        return LookUpUsername(is_taken=is_taken)


class LookUpUsernameMutation(graphene.ObjectType):
    lookup_username = LookUpUsername.Field()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        username_taken = get_user_model().objects.filter(username=username)
        if username_taken:
            raise GraphQLError(
                'This username is already in use')
        else:
            user = get_user_model()(
                username=username,
                email=email,
            )
            user.set_password(password)
            user.save()
            auth_user = authenticate(username=username, password=password)
            login(info.context, auth_user)
            token, _ = Token.objects.get_or_create(user=auth_user)
        return CreateUser(user=user, token=token)


class CreateUserMutation(graphene.ObjectType):
    create_user = CreateUser.Field()


class PauseAccount(graphene.Mutation):
    is_active = graphene.Boolean()

    class Arguments:
        pause_account = graphene.Boolean()

    def mutate(self, info, pause_account):
        user = info.context.user
        if pause_account:
            user.is_active = False
            user.save()
        else:
            user.is_active = True
            user.save()
        return PauseAccount(is_active=user.is_active)


class PauseAccountMutation(graphene.ObjectType):
    pause_account = PauseAccount.Field()


class DeleteUser(graphene.Mutation):
    user_deleted = graphene.Boolean()

    def mutate(self, info):
        user = info.context.user
        user.delete()
        return DeleteUser(user_deleted=True)


class DeleteUserMutation(graphene.ObjectType):
    delete_user = DeleteUser.Field()


class UpdateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    errors = graphene.String()

    class Arguments:
        username = graphene.String(required=False)
        email = graphene.String(required=False)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)

    def mutate(self, info, username, email, first_name, last_name):
        try:
            user = info.context.user
        except user.DoesNotExist:
            return UpdateUser(errors='You must be logged in to make these changes')
        if username:
            user.username = username
        if email:
            user.email = email
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        user.save()
        return UpdateUser(user=user, errors=None)


class UpdateUserMutation(graphene.ObjectType):
    update_user = UpdateUser.Field()


class UploadProfileImage(graphene.Mutation):
    profile = graphene.NonNull(ProfileType)

    class Arguments:
        url = graphene.String()

    @staticmethod
    def mutate(root, info, url=None):
        user = info.context.user
        if user.is_anonymous:
            raise graphql.GraphqlError(
                'You must be logged in to change your profile image')
        else:
            user_profile = info.context.user.profile
            image = create_system_image(info, url)
            user_profile.profile_avatar = image.image
            user_profile.save()
            return UploadProfileImage(profile=user_profile)


class UploadProfileImageMutation(graphene.ObjectType):
    upload_profile_image = UploadProfileImage.Field()


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
        except get_user_model().DoesNotExist:
            return UpdateUserProfile(errors='Please Login')
        profile = user.profile
        if profile_avatar:
            profile.profile_avatar = profile_avatar
        if bio:
            profile.bio = bio
        if location:
            profile.location = location
        if birth_date:
            profile.birth_date = birth_date
        if interests:
            profile.interests = profile.interests.add(*interests)

        profile.save()

        return UpdateUserProfile(profile=profile, errors=None)


class UpdateUserProfileMutation(graphene.ObjectType):
    update_profile = UpdateUserProfile.Field()


class UpdateUserInterests(graphene.Mutation):
    interests = graphene.List(InterestType)
    errors = graphene.String()

    class Arguments:
        ids = graphene.List(graphene.ID)

    def mutate(self, info, ids):
        profile = info.context.user.profile
        new_interests = profile.interests.add(*ids)
        return UpdateUserInterests(interests=profile.interests.all(), errors=None)


class UpdateUserInterestsMutation(graphene.ObjectType):
    update_interests = UpdateUserInterests.Field()


class UpdateLocation(graphene.Mutation):
    location = graphene.String()

    class Arguments:
        location = graphene.String()

    def mutate(self, info, location):
        user = info.context.user
        if user:
            profile = user.profile
            profile.location = location
            profile.save()
            return UpdateLocation(location=profile.location)
        else:
            raise graphene.GraphQlError(
                'No User found please login to update your location')


class UpdateLocationMutation(graphene.ObjectType):
    update_location = UpdateLocation.Field()


class UpdatePrivacyPermission(graphene.Mutation):
    is_private = graphene.Boolean()
    errors = graphene.String()

    class Arguments:
        is_private = graphene.Boolean()

    def mutate(self, info, is_private):
        user = info.context.user
        if user:
            user_privacy = user.is_private = is_private
            user.save()
            return UpdatePrivacyPermission(is_private=user.is_private, errors=None)
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
            user.is_hidden = is_hidden
            user.save()
            return UpdateHiddenPermission(is_hidden=user.is_hidden, errors=None)
        else:
            return UpdateHiddenPermission(errors="User not found, please login or create an account")


class UpdateHiddenMutation(graphene.ObjectType):
    update_hidden_status = UpdateHiddenPermission.Field()

# Friendship Mutations


class RequestFriend(graphene.Mutation):
    errors = graphene.String()
    friendship_request = graphene.Field(FriendshipRequestType)

    class Arguments:
        friend_id = graphene.ID()

    def mutate(self, info, friend_id):
        _user = info.context.user
        friend = get_user_model().objects.get(pk=friend_id)

        if _user and friend:
            Friend.objects.add_friend(
                _user,
                friend,
                message=""
            )
        return RequestFriend(friendship_request=FriendshipRequest.objects.get(to_user=friend), errors=None)


class RequestFriendMutation(graphene.ObjectType):
    request_friend = RequestFriend.Field()


class AddFriend(graphene.Mutation):
    new_friend = graphene.Field(FriendType)
    errors = graphene.String()

    class Arguments:
        friend_id = graphene.ID()

    def mutate(self, info, friend_id):
        user = info.context.user
        friend = get_user_model().objects.get(pk=friend_id)
        is_private_or_hidden = friend.is_private or friend.is_hidden

        if not is_private_or_hidden:
            Friend.objects.get_or_create(
                from_user=user,
                to_user=friend,
            )
            new_friend = Friend.objects.get(
                to_user=friend, from_user=user)
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
        friend_id = graphene.ID()

    def mutate(self, info, friend_id):
        user = info.context.user
        friend = get_user_model().objects.get(pk=friend_id)
        are_friends = Friend.objects.are_friends(
            user, friend) == True

        if are_friends:
            Friend.objects.remove_friend(user, friend)
            friend_list = Friend.objects.friends(friend)
            are_friends = Friend.objects.are_friends(
                user, friend) == True
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
        id = graphene.String()

    def mutate(self, info, id):
        friend_request = FriendshipRequest.objects.get(
            id=id)
        request_user = get_user_model().objects.get(id=friend_request.from_user.id)
        friend_request.accept()
        new_friend = Friend.objects.get(
            to_user=info.context.user, from_user=request_user)
        accepted = Friend.objects.are_friends(
            request_user, info.context.user) == True

        return AcceptFriendRequest(
            new_friend=new_friend, accepted=accepted, errors=None)


class AcceptFriendRequestMutation(graphene.ObjectType):
    accept_friend_request = AcceptFriendRequest.Field()


class CancelFriendRequest(graphene.Mutation):
    friend_requests = graphene.List(FriendshipRequestType)

    class Arguments:
        friend_id = graphene.ID()

    def mutate(self, info, friend_id):
        try:
            user = info.context.user
            friend = get_user_model().objects.get(pk=friend_id)
        except user.DoesNotExist or friend.DoesNotExist:
            return CancelFriendRequest(friend_requests=Friend.objects.unrejected_requests(user=user))
        if user and friend:
            request_to_cancel = FriendshipRequest.objects.get(
                to_user=friend)
            request_to_cancel.cancel()
            return CancelFriendRequest(friend_requests=Friend.objects.unrejected_requests(user=user))


class CancelFriendRequestMutation(graphene.ObjectType):
    cancel_friend_request = CancelFriendRequest.Field()


class DeclineFriendRequest(graphene.Mutation):
    friend_requests = graphene.List(FriendshipRequestType)
    errors = graphene.String()

    class Arguments:
        friend_id = graphene.ID()

    def mutate(self, info, friend_id):
        try:
            user = info.context.user
            friend = get_user_model().objects.get(pk=friend_id)
            friend_request = FriendshipRequest.objects.get(
                to_user=friend)

            friend_request.reject()
            return DeclineFriendRequest(friend_requests=Friend.objects.unrejected_requests(user=user), errors=None)

        except user.DoesNotExist:
            return DeclineFriendRequest(errors="user no longer exists")


class DeclineFriendRequestMutation(graphene.ObjectType):
    decline_friend_request = DeclineFriendRequest.Field()
