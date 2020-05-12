import os
import requests
import graphene
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

from graphene import Boolean, ID, List, Mutation, NonNull, String
from graphene_file_upload.scalars import Upload
from social.models import Post
from django.core.files.uploadedfile import SimpleUploadedFile

from .types import ImageType
from ..models import Image as ModelImage


def create_system_image(info, file=None, post_id=None):
    user = info.context.user
    if post_id:
        try:
            post = Post.objects.get(id=post_id)
        except post.DoesNotExist:
            raise graphene.GraphQLError(f"{post_id} does not exist")
    else:
        post = None

    if file:
        image = ModelImage.create_new(
            user=user if not user.is_anonymous else None,
            post_file=file,
            process_jpeg=True,
            post=post)
    return image


class UploadFiles(graphene.Mutation):
    success = graphene.Boolean()
    images = NonNull(List(NonNull(ImageType)))
    post_id = String()

    class Arguments:
        files = Upload(required=True)
        post_id = String()

    def mutate(self, info, files, post_id):
        for file in files:
            images = []
            image = create_system_image(info, file, post_id)
            images = images.append(image)
        return UploadFiles(success=True, images=images, post_id=post_id)


class UploadFilesMutation(graphene.ObjectType):
    uploadFilesMutation = UploadFiles.Field()


class DeleteImage(Mutation):
    deleted = NonNull(Boolean)

    class Arguments:
        id = NonNull(ID)

    @staticmethod
    def mutate(root, info, id):
        try:
            image = ModelImage.objects.get(id=id)
            image.user = None
            image.delete()
            return DeleteImage(deleted=True)
        except ModelImage.DoesNotExist:
            return DeleteImage(deleted=False)


class ImageMutation(object):
    delete_image = DeleteImage.Field()
