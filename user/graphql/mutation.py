from django.contrib.auth import get_user_model, authenticate, login, logout
import graphene
from graphene import NonNull, List, Field, Mutation, ObjectType, String, Boolean, ID
from rest_framework.authtoken.models import Token
from graphql import GraphQLError
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
from friendship.models import Friend, Follow, Block, FriendshipRequest
from interests.models import Interest
from interests.graphql.types import InterestType
from social.graphql.types import FriendType, FriendshipRequestType
from system.graphql.types import ImageType
from system.graphql.mutation import create_system_image
from .types import UserType, ProfileType
from ..models import Profile


class LoginUser(Mutation):
    success = NonNull(Boolean)
    account = Field(UserType)
    token = String()
    message = String()

    class Arguments:
        username = NonNull(String)
        password = NonNull(String)

    @staticmethod
    def mutate(root, info, username, password):
        user = authenticate(username=username, password=password)
        if not user:
            return LoginUser(success=False, message="Invalid Credentials")
        login(info.context, user)
        token, _ = Token.objects.get_or_create(user=user)
        return LoginUser(success=True, account=user, token=token)


class LoginUserMutation(ObjectType):
    user_login = LoginUser.Field()


class LogoutUser(Mutation):
    success = NonNull(Boolean)

    class Arguments:
        pass

    @staticmethod
    def mutate(root, info):
        logout(info.context)
        return LogoutUser(success=True)


class LogoutUserMutation(ObjectType):
    user_logout = LogoutUser.Field()


class LookUpUsername(Mutation):
    is_taken = Boolean()

    class Arguments:
        username = String(required=True)

    def mutate(self, info, username):
        is_taken = get_user_model().objects.filter(username=username)
        return LookUpUsername(is_taken=is_taken)


class LookUpUsernameMutation(ObjectType):
    lookup_username = LookUpUsername.Field()


class CreateUser(Mutation):
    user = Field(UserType)
    token = String()

    class Arguments:
        username = String(required=True)
        password = String(required=True)
        email = String(required=True)

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


class CreateUserMutation(ObjectType):
    create_user = CreateUser.Field()


class PauseAccount(Mutation):
    is_active = Boolean()

    class Arguments:
        pause_account = Boolean()

    def mutate(self, info, pause_account):
        user = info.context.user
        if pause_account:
            user.is_active = False
            user.save()
        else:
            user.is_active = True
            user.save()
        return PauseAccount(is_active=user.is_active)


class PauseAccountMutation(ObjectType):
    pause_account = PauseAccount.Field()


class DeleteUser(Mutation):
    user_deleted = Boolean()

    def mutate(self, info):
        user = info.context.user
        user.delete()
        return DeleteUser(user_deleted=True)


class DeleteUserMutation(ObjectType):
    delete_user = DeleteUser.Field()


class UpdateUser(Mutation):
    user = Field(UserType)
    errors = String()

    class Arguments:
        username = String(required=False)
        email = String(required=False)
        first_name = String(required=False)
        last_name = String(required=False)
        phone_number = String(required=False)

    def mutate(self, info, username, email, first_name, last_name, phone_number):
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
        if phone_number:
            user.phone_number = phone_number
        user.save()
        return UpdateUser(user=user, errors=None)


class UpdateUserMutation(ObjectType):
    update_user = UpdateUser.Field()


class UploadProfileImage(Mutation):
    profile_image = Field(ImageType)

    class Arguments:
        profile_image = Upload(required=True)

    @staticmethod
    def mutate(root, info, profile_image):
        user = info.context.user
        if user.is_anonymous:
            raise graphql.GraphqlError(
                'You must be logged in to change your profile image')
        else:
            user_profile = info.context.user.profile
            image = create_system_image(info, profile_image, post_id=None)
            user_profile.profile_avatar = image
            user_profile.save()
            return UploadProfileImage(profile_image=user_profile.profile_avatar)


class UploadProfileImageMutation(ObjectType):
    upload_profile_image = UploadProfileImage.Field()


class UpdateUserProfile(Mutation):
    errors = String()
    profile = Field(ProfileType)

    class Arguments:
        avatar_image = Upload(required=False)
        bio = String(required=False)
        birth_date = graphene.types.datetime.Date(required=False)
        location = String(required=False)
        interests = List(ID, required=False)

    def mutate(self, info, avatar_image, bio, location, birth_date, interests):
        try:
            user = info.context.user
        except get_user_model().DoesNotExist:
            return UpdateUserProfile(errors='Please Login')
        profile = user.profile
        if avatar_image:
            image = create_system_image(info, avatar_image, post_id=None)
            user_profile.profile_avatar = image
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


class UpdateUserProfileMutation(ObjectType):
    update_profile = UpdateUserProfile.Field()


class UpdateUserInterests(Mutation):
    interests = List(InterestType)
    errors = String()

    class Arguments:
        ids = List(ID)

    def mutate(self, info, ids):
        profile = info.context.user.profile
        new_interests = profile.interests.add(*ids)
        return UpdateUserInterests(interests=profile.interests.all(), errors=None)


class UpdateUserInterestsMutation(ObjectType):
    update_interests = UpdateUserInterests.Field()


class UpdateLocation(Mutation):
    location = String()

    class Arguments:
        location = String()

    def mutate(self, info, location):
        user = info.context.user
        if user:
            profile = user.profile
            profile.location = location
            profile.save()
            return UpdateLocation(location=profile.location)
        else:
            raise GraphQlError(
                'No User found please login to update your location')


class UpdateLocationMutation(ObjectType):
    update_location = UpdateLocation.Field()


class UpdatePrivacyPermission(Mutation):
    is_private = Boolean()
    errors = String()

    class Arguments:
        is_private = Boolean()

    def mutate(self, info, is_private):
        user = info.context.user
        if user:
            user_privacy = user.is_private = is_private
            user.save()
            return UpdatePrivacyPermission(is_private=user.is_private, errors=None)
        else:
            return UpdatePrivacyPermission(errors="User not found, please login or create an account")


class UpdatePrivacyMutation(ObjectType):
    update_privacy_status = UpdatePrivacyPermission.Field()


class UpdateHiddenPermission(Mutation):
    is_hidden = Boolean()
    errors = String()

    class Arguments:
        is_hidden = Boolean()

    def mutate(self, info, is_hidden):
        user = info.context.user
        if user:
            user.is_hidden = is_hidden
            user.save()
            return UpdateHiddenPermission(is_hidden=user.is_hidden, errors=None)
        else:
            return UpdateHiddenPermission(errors="User not found, please login or create an account")


class UpdateHiddenMutation(ObjectType):
    update_hidden_status = UpdateHiddenPermission.Field()

# Friendship Mutations


class CreateFriendRequest(Mutation):
    friendship_request = Field(FriendshipRequestType)

    class Arguments:
        friend_id = ID()

    def mutate(self, info, friend_id):
        user = info.context.user
        friend = get_user_model().objects.get(pk=friend_id)
        if user and friend:
            Friend.objects.add_friend(
                user,
                friend,
                message=""
            )
        return CreateFriendRequest(friendship_request=FriendshipRequest.objects.get(to_user=friend))


class CreateFriendRequestMutation(ObjectType):
    create_friend_request = CreateFriendRequest.Field()


class AddFriend(Mutation):
    new_friend = Field(UserType)
    errors = String()

    class Arguments:
        friend_id = ID()

    def mutate(self, info, friend_id):
        user = info.context.user
        friend = get_user_model().objects.get(pk=friend_id)
        is_private_or_hidden = friend.is_private or friend.is_hidden

        if not is_private_or_hidden:
            Friend.objects.get_or_create(
                from_user=user,
                to_user=friend,
            )
            Follow.objects.add_follower(user, friend)
            Follow.objects.add_follower(friend, user)

            return AddFriend(new_friend=friend, errors=None)
        else:
            CreateFriendRequest(friend_id=friend_id)
            return AddFriend(errors="This user is private, We have created a friendship request for you")


class AddFriendMutation(ObjectType):
    add_friend = AddFriend.Field()


class RemoveFriend(Mutation):
    success = Boolean()
    errors = String()

    class Arguments:
        friend_id = ID()

    def mutate(self, info, friend_id):
        user = info.context.user
        friend = get_user_model().objects.get(pk=friend_id)
        Follow.objects.remove_follower(user, friend)
        Follow.objects.remove_follower(friend, user)
        Friend.objects.remove_friend(user, friend)

        return RemoveFriend(success=True)


class RemoveFriendMutation(ObjectType):
    remove_friend = RemoveFriend.Field()


class AcceptFriendRequest(Mutation):
    new_friend = Field(UserType)
    accepted = Boolean()
    errors = String()

    class Arguments:
        id = String()

    def mutate(self, info, id):
        user = info.context.user
        friend_request = FriendshipRequest.objects.get(
            id=id)
        friend = get_user_model().objects.get(
            id=friend_request.from_user.id)
        friend_request.accept()
        Follow.objects.add_follower(user, friend)
        Follow.objects.add_follower(friend, user)
        return AcceptFriendRequest(
            new_friend=friend, accepted=Friend.objects.are_friends(
                friend, user) == True, errors=None)


class AcceptFriendRequestMutation(ObjectType):
    accept_friend_request = AcceptFriendRequest.Field()


class CancelFriendRequest(Mutation):
    friend_requests = List(FriendshipRequestType)

    class Arguments:
        friend_id = ID()

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


class CancelFriendRequestMutation(ObjectType):
    cancel_friend_request = CancelFriendRequest.Field()


class DeclineFriendRequest(Mutation):
    friend_requests = List(FriendshipRequestType)
    errors = String()

    class Arguments:
        friend_id = ID()

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


class DeclineFriendRequestMutation(ObjectType):
    decline_friend_request = DeclineFriendRequest.Field()
