from django.db import models
import graphene
from graphene import List, Schema, ObjectType, NonNull, ID
from graphene_django import DjangoObjectType
from address.mutation import UpdateAddressMutation
from interests.graphql.query import InterestListQuery, GetInterests
from social.graphql.query import PostsQuery, GetPostQuery, GetPostCommentsQuery, GetPostLikesQuery
from social.graphql.mutation import AddPostMutation, UpdatePostMutation, DeletePostMutation, LikePostMutation, RemoveLikePostMutation, AddPostCommentMutation, UpdatePostCommentMutation, DeletePostCommentMutation
from user.query import UserListQuery, UserQuery, UserSearchQuery
from user.mutation import LoginUserMutation, LogoutUserMutation, AddFriendMutation, RemoveFriendMutation, CreateUserMutation, CancelFriendRequestMutation, RequestFriendMutation, AcceptFriendRequestMutation, DeclineFriendRequestMutation, UpdateUserMutation, UpdateUserProfileMutation, UpdatePrivacyMutation, UpdateHiddenMutation, UpdateUserInterestsMutation


class Query(
    GetInterests,
    InterestListQuery,
    GetPostQuery,
    GetPostLikesQuery,
    PostsQuery,
    GetPostCommentsQuery,
    UserListQuery,
    UserQuery,
    UserSearchQuery
):
    pass


class Mutation(
    AddPostMutation,
    UpdatePostMutation,
    DeletePostMutation,
    LikePostMutation,
    RemoveLikePostMutation,
    AddPostCommentMutation,
    UpdatePostCommentMutation,
    DeletePostCommentMutation,
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
