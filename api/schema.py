from django.db import models
import graphene
from graphene import List, Schema, ObjectType, NonNull, ID
from graphene_django import DjangoObjectType
from address.graphql.mutation import UpdateAddressMutation
from address.graphql.query import CountryQuery
from interests.graphql.query import InterestListQuery, GetInterests
from invites.graphql.mutation import CreateInviteMutation, UpdateInviteMutation, DeleteInviteMutation, ClaimInviteMutation, CreateUserFromInviteMutation
from social.graphql.query import PostsQuery, FeedQuery, GetPostQuery, GetPostCommentsQuery, GetPostLikesQuery
from social.graphql.mutation import AddPostMutation, UpdatePostMutation, DeletePostMutation, LikePostMutation, RemoveLikePostMutation, AddPostCommentMutation, UpdatePostCommentMutation, DeletePostCommentMutation
from system.graphql.mutation import ImageMutation, UploadMutation
from user.graphql.query import GetAuthUserQuery, GetUserProfileQuery, ProfileSearchQuery, GetAuthUserProfileQuery
from user.graphql.mutation import LoginUserMutation, LogoutUserMutation, UpdateLocationMutation, AddFriendMutation, RemoveFriendMutation, CreateUserMutation, PauseAccountMutation, DeleteUserMutation, CancelFriendRequestMutation, CreateFriendRequestMutation, AcceptFriendRequestMutation, DeclineFriendRequestMutation, UpdateUserMutation, UpdateUserProfileMutation, UploadProfileImageMutation, UpdatePrivacyMutation, UpdateHiddenMutation, UpdateUserInterestsMutation, LookUpUsernameMutation


class Query(
    CountryQuery,
    GetAuthUserQuery,
    GetInterests,
    InterestListQuery,
    GetPostQuery,
    GetPostLikesQuery,
    PostsQuery,
    FeedQuery,
    GetPostCommentsQuery,
    GetAuthUserProfileQuery,
    GetUserProfileQuery,
    ProfileSearchQuery,
):
    pass


class Mutation(
    UploadMutation,
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
    CreateFriendRequestMutation,
    AcceptFriendRequestMutation,
    CancelFriendRequestMutation,
    DeclineFriendRequestMutation,
    ImageMutation,
    LookUpUsernameMutation
):
    pass


schema = Schema(query=Query, mutation=Mutation)
