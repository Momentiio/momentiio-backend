import os
import datetime
import PIL.Image as pil
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from momentiio.storages import PrivateMediaStorage


def image_path_generator(instance, filename):
    __, ext = os.path.splitext(filename)
    if instance.user:
        path = os.path.join(
            'user_images',
            str(instance.user.username)
        )
    else:
        path = os.path.join(
            'system_images',
            datetime.datetime.now().strftime('%Y/%-m/%-d')
        )
    return os.path.join(
        path,
        filename
    ).lower()


class Image(models.Model):
    image = models.ImageField(upload_to=image_path_generator)
    user = models.ForeignKey(
        get_user_model(), related_name='images', on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.image}"

    def get_absolute_url(self):
        return self.image.image

    @classmethod
    def create_new(cls, user=None, post_file=None, localfilename=None,
                   update_existing=False, process_jpeg=True):

        if update_existing:
            image = update_existing
        else:
            image = Image(user=user)

        if localfilename:
            pil.open(localfilename).verify()
            with open(localfilename, 'rb') as fh:
                image.image = SimpleUploadedFile(
                    name=os.path.basename(localfilename),
                    content=fh.read())

        elif post_file:
            image.image = post_file

        else:
            raise ValueError("'post_file' or 'localfilename' is required")

        image.save()

        return image
