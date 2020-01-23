import os
import requests
import graphene
from graphene import Boolean, ID, List, Mutation, NonNull, String
from graphene_file_upload.scalars import Upload
from social.models import Post
from django.core.files.uploadedfile import SimpleUploadedFile

from .types import ImageType
from ..models import Image


def create_system_image(info, url=None, file=None, post_id=None):
    user = info.context.user

    if post_id:
        post = Post.objects.get(id=post_id)
    else:
        post = None

    if file:
        image_file = SimpleUploadedFile(
            name=os.path.basename(file.name)[0],
            content=file.content
        )

    elif url:
        image_file = SimpleUploadedFile(
            name=os.path.basename(url).split('?')[0],
            content=requests.get(url).content
        )

    else:
        image_file = info.context.FILES['image_file']

    image = Image.create_new(
        user=user if not user.is_anonymous else None,
        post_file=image_file,
        process_jpeg=True,
        post=post)

    return image


class UploadMutation(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        files = Upload(required=True)
        post_id = String()

    def mutate(self, info, files, post_id):
        for file in files:
            file = create_system_image(info, file, post_id)
        return UploadMutation(success=True)


class UploadImageFromUrl(Mutation):
    image = NonNull(ImageType)

    class Arguments:
        url = String()

    @staticmethod
    def mutate(root, info, url=None):
        image = create_system_image(info, url)
        return UploadImage(image=image)


class DeleteImage(Mutation):
    deleted = NonNull(Boolean)

    class Arguments:
        id = NonNull(ID)

    @staticmethod
    def mutate(root, info, id):
        try:
            image = Image.objects.get(id=id)
            image.user = None
            image.save()
            return DeleteImage(deleted=True)
        except Image.DoesNotExist:
            return DeleteImage(deleted=False)


class ImageMutation(object):
    upload_image = UploadMutation.Field()
    delete_image = DeleteImage.Field()
