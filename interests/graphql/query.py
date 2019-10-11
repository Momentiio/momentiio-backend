from django.db import models
import graphene
from .types import InterestType
from interests.models import Interest


class InterestListQuery(graphene.ObjectType):
    interests = graphene.NonNull(graphene.List(InterestType))

    def resolve_interests(self, info):
        return Interest.objects.all()


class GetInterests(graphene.ObjectType):
    interest_list = graphene.List(
        InterestType, interests=graphene.List(graphene.ID))

    def resolve_interest_list(self, info, interests):
        return Interest.objects.filter(pk__in=interests)
