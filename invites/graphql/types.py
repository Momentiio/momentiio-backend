import graphene
from graphene_django import DjangoObjectType
from ..models import Invite


class InviteType(DjangoObjectType):
    class Meta:
        model = Invite
        only_fields = (
            "id",
            "token",
            "sponsor",
            "created_at",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "avatar",
            "note",
            "expiration"
        )
