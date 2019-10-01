from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from interests.models import Interest
from .models import Profile
from .query import ProfileType, UserType


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
    class Arguments:
        user_id = graphene.ID()
        username = graphene.String()
        email = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
    user = graphene.Field(UserType)
    errors = graphene.String()

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
    class Arguments:
        user_id = graphene.ID()
        profile_avatar = graphene.String()
        bio = graphene.String()
        birth_date = graphene.types.datetime.Date()
        location = graphene.String()
        # interests = graphene.List(InterestType)

    errors = graphene.String()
    profile = graphene.Field(ProfileType)

    def mutate(self, info, user_id, profile_avatar, bio, location, birth_date):
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
        # if interests is not None:
        #     profile.interests = interests

        profile.save()

        return UpdateUserProfile(profile=profile, errors=None)


class UpdateUserProfileMutation(graphene.ObjectType):
    update_profile = UpdateUserProfile.Field()
