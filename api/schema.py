from django.db import models
import graphene
from graphene import List, Schema, ObjectType, NonNull, ID
from graphene_django import DjangoObjectType
from address.mutation import UpdateAddressMutation
from social.query import PostsQuery
from user.query import UserListQuery, UserQuery
from user.mutation import CreateUserMutation, CancelFriendRequestMutation, RequestFriendMutation, AcceptFriendRequestMutation, DeclineFriendRequestMutation, UserAuth, UpdateUserMutation, UpdateUserProfileMutation


class Query(
    PostsQuery,
    UserListQuery,
    UserQuery
):
    pass


class Mutation(
    AcceptFriendRequestMutation,
    CreateUserMutation,
    RequestFriendMutation,
    CancelFriendRequestMutation,
    DeclineFriendRequestMutation,
    UpdateAddressMutation,
    UpdateUserMutation,
    UpdateUserProfileMutation,
    UserAuth
):
    pass


schema = Schema(query=Query, mutation=Mutation)
