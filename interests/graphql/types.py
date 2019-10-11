from django.db import models
import graphene
from graphene_django import DjangoObjectType
from interests.models import Interest


class InterestType(DjangoObjectType):
    class Meta:
        model = Interest
        only_fields = {
            "id",
            "title",
            "photo",
            "category"
        }
