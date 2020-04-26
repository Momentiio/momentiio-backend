from django.db import models
import graphene
from graphene import List, Schema, ObjectType, NonNull, ID
from graphene_django import DjangoObjectType
from address.graphql.mutation import UpdateAddressMutation
from address.graphql.query import CountryQuery
from interests.graphql.query import InterestListQuery, GetInterests
from invites.graphql.mutation import CreateInviteMutation, UpdateInviteMutation, DeleteInviteMutation, ClaimInviteMutation, CreateUserFromInviteMutation
from social.graphql.query import PostsQuery, FeedQuery, GetPostQuery, GetPostCommentsQuery, GetPostLikesQuery
from social.graphql.mutation import CreatePostMutation, UpdatePostMutation, DeletePostMutation, LikePostMutation, RemoveLikePostMutation, AddPostCommentMutation, UpdatePostCommentMutation, DeletePostCommentMutation
from system.graphql.query import ImageFilterQuery
from system.graphql.mutation import UploadFilesMutation, ImageMutation
from user.graphql.query import GetAuthUserQuery, GetUserProfileQuery, UserSearchQuery, GetAuthUserProfileQuery, GetAuthUserImages, GetFriendRequests
from user.graphql.mutation import LoginUserMutation, LogoutUserMutation, UpdateLocationMutation, AddFriendMutation, RemoveFriendMutation, CreateUserMutation, PauseAccountMutation, DeleteUserMutation, CancelFriendRequestMutation, CreateFriendRequestMutation, AcceptFriendRequestMutation, DeclineFriendRequestMutation, UpdateUserMutation, UpdateUserProfileMutation, UploadProfileImageMutation, UpdatePrivacyMutation, UpdateHiddenMutation, UpdateUserInterestsMutation, LookUpUsernameMutation


class Query(
    CountryQuery,
    GetAuthUserQuery,
    GetAuthUserImages,
    GetInterests,
    InterestListQuery,
    GetPostQuery,
    GetPostLikesQuery,
    PostsQuery,
    FeedQuery,
    GetPostCommentsQuery,
    GetAuthUserProfileQuery,
    GetUserProfileQuery,
    UserSearchQuery,
    GetFriendRequests,
    ImageFilterQuery
):
    pass


class Mutation(
    UploadFilesMutation,
    CreateInviteMutation,
    UpdateInviteMutation,
    DeleteInviteMutation,
    ClaimInviteMutation,
    CreateUserFromInviteMutation,
    CreatePostMutation,
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
