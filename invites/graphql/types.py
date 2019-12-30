import graphene
from graphene_django import DjangoObjectType
from ..models import InviteUser


class InviteUserType(DjangoObjectType):
    class Meta:
        model = InviteUser
        only_fields = (
            "id",
            "sponsor",
            "created_at",
            "name",
            "email",
            "phone_number",
            "avatar",
            "note",
            "expiration"
        )
