from django.db import models
from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType
from system.graphql.mutation import create_system_image
from .types import InviteUserType
from ..models import InviteUser


class CreateInvite(graphene.Mutation):
    created_invitation = graphene.Field(InviteUserType)

    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=False)
        phone = graphene.String(required=False)
        note = graphene.String(required=False)
        avatar = graphene.String(required=False)

    def mutate(self, info, name, email, phone, note, avatar):
        sponsor = info.context.user
        invite = InviteUser.objects.create(
            name=name,
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


class DeleteInvite(graphene.Mutation):
    is_deleted = graphene.Boolean()

    class Arguments:
        invite_id = graphene.ID()

    def mutate(self, info, invite_id):
        invite = InviteUser.objects.filter(id=invite_id)
        invite.delete()
        return DeleteInvite(is_deleted=True)


class DeleteInviteMutation(graphene.ObjectType):
    delete_invite = DeleteInvite.Field()
