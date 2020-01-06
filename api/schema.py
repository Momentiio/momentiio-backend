from django.db import models
import graphene
from graphene import List, Schema, ObjectType, NonNull, ID
from graphene_django import DjangoObjectType
from address.graphql.mutation import UpdateAddressMutation
from interests.graphql.query import InterestListQuery, GetInterests
from invites.graphql.mutation import CreateInviteMutation, DeleteInviteMutation
from social.graphql.query import PostsQuery, GetPostQuery, GetPostCommentsQuery, GetPostLikesQuery
from social.graphql.mutation import AddPostMutation, UpdatePostMutation, DeletePostMutation, LikePostMutation, RemoveLikePostMutation, AddPostCommentMutation, UpdatePostCommentMutation, DeletePostCommentMutation
from system.graphql.mutation import ImageMutation
from user.graphql.query import GetAuthUserQuery, GetUserProfileQuery, UserSearchQuery, GetAuthUserProfileQuery
from user.graphql.mutation import LoginUserMutation, LogoutUserMutation, AddFriendMutation, RemoveFriendMutation, CreateUserMutation, DeleteUserMutation, CancelFriendRequestMutation, RequestFriendMutation, AcceptFriendRequestMutation, DeclineFriendRequestMutation, UpdateUserMutation, UpdateUserProfileMutation, UploadProfileImageMutation, UpdatePrivacyMutation, UpdateHiddenMutation, UpdateUserInterestsMutation, LookUpUsernameMutation


class Query(
    GetAuthUserQuery,
    GetInterests,
    InterestListQuery,
    GetPostQuery,
    GetPostLikesQuery,
    PostsQuery,
    GetPostCommentsQuery,
    GetAuthUserProfileQuery,
    GetUserProfileQuery,
    UserSearchQuery
):
    pass


class Mutation(
    CreateInviteMutation,
    DeleteInviteMutation,
    AddPostMutation,
    UpdatePostMutation,
    DeletePostMutation,
    LikePostMutation,
    RemoveLikePostMutation,
    AddPostCommentMutation,
    UpdatePostCommentMutation,
    DeletePostCommentMutation,
    CreateUserMutation,
    DeleteUserMutation,
    LoginUserMutation,
    LogoutUserMutation,
    UpdateAddressMutation,
    UpdateUserMutation,
    UpdateUserProfileMutation,
    UploadProfileImageMutation,
    UpdateUserInterestsMutation,
    UpdatePrivacyMutation,
    UpdateHiddenMutation,
    AddFriendMutation,
    RemoveFriendMutation,
    RequestFriendMutation,
    AcceptFriendRequestMutation,
    CancelFriendRequestMutation,
    DeclineFriendRequestMutation,
    ImageMutation,
    LookUpUsernameMutation
):
    pass


schema = Schema(query=Query, mutation=Mutation)
