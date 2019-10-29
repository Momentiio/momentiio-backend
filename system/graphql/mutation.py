import os
import requests
import graphene

from graphene import Boolean, ID, List, Mutation, NonNull, String
from django.core.files.uploadedfile import SimpleUploadedFile

from .types import ImageType
from ..models import Image


def create_system_image(info, url=None):
    user = info.context.user
    if url:
        image_file = SimpleUploadedFile(
            name=os.path.basename(url).split('?')[0],
            content=requests.get(url).content
        )
    else:
        image_file = info.context.FILES['image_file']
    image = Image.create_new(
        user=user if not user.is_anonymous else None,
        post_file=image_file,
        process_jpeg=True
    )

    return image


class UploadImage(Mutation):
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
    upload_image = UploadImage.Field()
    delete_image = DeleteImage.Field()
