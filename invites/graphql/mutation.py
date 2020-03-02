import secrets
from django.db import models
from django.contrib.auth import get_user_model
from graphql import GraphQLError
import graphene
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
from user.graphql.types import UserType
from system.graphql.mutation import create_system_image
from .types import InviteType
from ..models import Invite


class CreateInvite(graphene.Mutation):
    created_invitation = graphene.Field(InviteType)

    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=False)
        phone = graphene.String(required=False)
        note = graphene.String(required=False)
        avatar_image = Upload(required=False)

    def mutate(self, info, first_name, last_name, email, phone, note):
        sponsor = info.context.user
        users = get_user_model().objects.all()
        for user in users:
            if user.email == email:
                raise GraphQLError('This email already has an account')
            elif user.phone_number == phone:
                raise GraphQLError(
                    'This phone number is already attached to an account')
            else:
                pass

        else:
            avatar = None

        invite = Invite.objects.create(
            token=secrets.token_urlsafe(20),
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone,
            note=note,
            avatar=avatar,
            sponsor=sponsor.id,
        )
        invite.save()
        sponsor_invites = sponsor.invites.add(invite)
        return CreateInvite(created_invitation=invite)


class CreateInviteMutation(graphene.ObjectType):
    create_invite = CreateInvite.Field()


class ClaimInvite(graphene.Mutation):
    invite = graphene.Field(InviteType)

    class Arguments:
        invite_token = graphene.String()

    def mutate(self, info, invite_token):
        try:
            invite = Invite.objects.get(token=invite_token)
            if invite.is_expired():
                invite.delete()
                raise graphene.GraphQLError('Your Invite has expired')
        except invite.DoesNotExist:
            raise graphene.GraphQLError('This is not a valid Invite code')
        return ClaimInvite(invite=invite)


class ClaimInviteMutation(graphene.ObjectType):
    claim_invite = ClaimInvite.Field()


class UpdateInvite(graphene.Mutation):
    invite = graphene.Field(InviteType)

    class Arguments:
        invite_id = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        phone_number = graphene.String()
        avatar_image = Upload(required=False)

    def mutate(self, info, invite_id, first_name, last_name, email, phone_number, avatar_image):
        try:
            invite = Invite.objects.get(id=invite_id)
        except invite.DoesNotExist:
            raise graphene.GraphQLError('Looks like this invite is invalid')
        if first_name:
            invite.first_name = first_name
        if last_name:
            invite.last_name = last_name
        if email:
            invite.email = email
        if phone_number:
            invite.phone_number = phone_number
        if avatar_image:
            image = create_system_image(info, avatar_image, post_id=None)
            invite.avatar = image
        invite.save()
        return UpdateInvite(invite=invite)


class UpdateInviteMutation(graphene.ObjectType):
    update_invite = UpdateInvite.Field()


class DeleteInvite(graphene.Mutation):
    is_deleted = graphene.Boolean()

    class Arguments:
        invite_id = graphene.ID()

    def mutate(self, info, invite_id):
        invite = Invite.objects.filter(id=invite_id)
        invite.delete()
        return DeleteInvite(is_deleted=True)


class DeleteInviteMutation(graphene.ObjectType):
    delete_invite = DeleteInvite.Field()


class CreateUserFromInvite(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        invite_id = graphene.String()
        username = graphene.String()
        password = graphene.String()

    def mutate(self, info, invite_id, username, password):
        try:
            invite = Invite.objects.get(id=invite_id)
            new_user = get_user_model()(
                username=username,
                email=invite.email,
                phone_number=invite.phone_number,
                first_name=invite.first_name,
                last_name=invite.last_name,
                sponsor=invite.sponsor
            )
            new_user.set_password(password)
            new_user.save()
            profile = new_user.profile
            profile.profile_avatar = invite.avatar
            profile.save()
            invite.delete()
        except invite.DoesNotExist:
            raise graphene.GraphQLError(
                'The invite you are trying to access is invalid')

        return CreateUserFromInvite(user=new_user)


class CreateUserFromInviteMutation(graphene.ObjectType):
    create_user_from_invite = CreateUserFromInvite.Field()
