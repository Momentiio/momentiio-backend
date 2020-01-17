from django.db import models
import graphene
from graphene import List, Schema, ObjectType, NonNull, ID
from graphene_django import DjangoObjectType
from address.graphql.mutation import UpdateAddressMutation
from interests.graphql.query import InterestListQuery, GetInterests
from invites.graphql.mutation import CreateInviteMutation, UpdateInviteMutation, DeleteInviteMutation, ClaimInviteMutation, CreateUserFromInviteMutation
from social.graphql.query import PostsQuery, GetPostQuery, GetPostCommentsQuery, GetPostLikesQuery
from social.graphql.mutation import AddPostMutation, UpdatePostMutation, DeletePostMutation, LikePostMutation, RemoveLikePostMutation, AddPostCommentMutation, UpdatePostCommentMutation, DeletePostCommentMutation
from system.graphql.mutation import ImageMutation
from user.graphql.query import GetAuthUserQuery, GetUserProfileQuery, ProfileSearchQuery, UserSearchQuery, GetAuthUserProfileQuery
from user.graphql.mutation import LoginUserMutation, LogoutUserMutation, UpdateLocationMutation, AddFriendMutation, RemoveFriendMutation, CreateUserMutation, PauseAccountMutation, DeleteUserMutation, CancelFriendRequestMutation, RequestFriendMutation, AcceptFriendRequestMutation, DeclineFriendRequestMutation, UpdateUserMutation, UpdateUserProfileMutation, UploadProfileImageMutation, UpdatePrivacyMutation, UpdateHiddenMutation, UpdateUserInterestsMutation, LookUpUsernameMutation


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
    ProfileSearchQuery,
    UserSearchQuery,
):
    pass


class Mutation(
    CreateInviteMutation,
    UpdateInviteMutation,
    DeleteInviteMutation,
    ClaimInviteMutation,
    CreateUserFromInviteMutation,
    AddPostMutation,
    UpdatePostMutation,
    DeletePostMutation,
    LikePostMutation,
    RemoveLikePostMutation,
    AddPostCommentMutation,
    UpdatePostCommentMutation,
    DeletePostCommentMutation,
    CreateUserMutation,
    PauseAccountMutation,
    DeleteUserMutation,
    LoginUserMutation,
    LogoutUserMutation,
    UpdateAddressMutation,
    UpdateUserMutation,
    UpdateLocationMutation,
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
