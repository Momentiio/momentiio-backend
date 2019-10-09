from django.db import models
import graphene
from graphene import List, Schema, ObjectType, NonNull, ID
from graphene_django import DjangoObjectType
from address.mutation import UpdateAddressMutation
from social.query import PostsQuery
from user.query import UserListQuery, UserQuery
from user.mutation import LoginUserMutation, LogoutUserMutation, AddFriendMutation, RemoveFriendMutation, CreateUserMutation, CancelFriendRequestMutation, RequestFriendMutation, AcceptFriendRequestMutation, DeclineFriendRequestMutation, UpdateUserMutation, UpdateUserProfileMutation, UpdatePrivacyMutation, UpdateHiddenMutation


class Query(
    PostsQuery,
    UserListQuery,
    UserQuery
):
    pass


class Mutation(
    CreateUserMutation,
    LoginUserMutation,
    LogoutUserMutation,
    UpdateAddressMutation,
    UpdateUserMutation,
    UpdateUserProfileMutation,
    UpdatePrivacyMutation,
    UpdateHiddenMutation,
    AddFriendMutation,
    RemoveFriendMutation,
    RequestFriendMutation,
    AcceptFriendRequestMutation,
    CancelFriendRequestMutation,
    DeclineFriendRequestMutation
):
    pass


schema = Schema(query=Query, mutation=Mutation)
