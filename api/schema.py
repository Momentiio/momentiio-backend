from django.db import models
import graphene
from graphene import List, Schema, ObjectType, NonNull, ID
from graphene_django import DjangoObjectType
from address.mutation import UpdateAddressMutation
from interests.graphql.query import InterestListQuery, GetInterests
from social.graphql.query import PostsQuery
from social.graphql.mutation import AddPostMutation, UpdatePostMutation, DeletePostMutation
from user.query import UserListQuery, UserQuery
from user.mutation import LoginUserMutation, LogoutUserMutation, AddFriendMutation, RemoveFriendMutation, CreateUserMutation, CancelFriendRequestMutation, RequestFriendMutation, AcceptFriendRequestMutation, DeclineFriendRequestMutation, UpdateUserMutation, UpdateUserProfileMutation, UpdatePrivacyMutation, UpdateHiddenMutation, UpdateUserInterestsMutation


class Query(
    GetInterests,
    InterestListQuery,
    PostsQuery,
    UserListQuery,
    UserQuery
):
    pass


class Mutation(
    AddPostMutation,
    UpdatePostMutation,
    DeletePostMutation,
    CreateUserMutation,
    LoginUserMutation,
    LogoutUserMutation,
    UpdateAddressMutation,
    UpdateUserMutation,
    UpdateUserProfileMutation,
    UpdateUserInterestsMutation,
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
