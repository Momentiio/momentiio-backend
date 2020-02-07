import os
import datetime
import PIL.Image as pil
from io import BytesIO
from django.core.files import File
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from social.models import Post


def compress(image):
    im = pil.open(image)
    im = im.convert('RGB')
    im.save(image)
    im_io = BytesIO()
    im.save(im_io, "JPEG", quality=60)
    new_image = File(im_io, name=image.name)
    return new_image


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
    image_height = models.IntegerField(default=0)
    image_width = models.IntegerField(default=0)
    image = models.ImageField(upload_to=image_path_generator,
                              height_field="image_height", width_field="image_width")
    post = models.ForeignKey(
        Post, related_name="post_images", null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(
        get_user_model(), related_name='user_images', on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.image}"

    def get_absolute_url(self):
        return self.image.url

    @classmethod
    def create_new(cls, user=None, post=None, post_file=None, localfilename=None,
                   update_existing=False, process_jpeg=True):

        if update_existing:
            image = update_existing
        else:
            image = Image(user=user, post=post)

        if localfilename:
            pil.open(localfilename).verify()
            with open(localfilename, 'rb') as fh:
                image.image = SimpleUploadedFile(
                    name=os.path.basename(localfilename),
                    content=fh.read())
                image.post = post

        elif post_file:
            new_image = compress(post_file)
            image.image = new_image
            image.post = post

        else:
            raise ValueError("'post_file' or 'localfilename' is required")

        image.save()

        return image


class ImageFilter(models.Model):
    name = models.CharField(max_length=25)
    filter = models.CharField(max_length=100, null=True)
    background = models.CharField(max_length=250, null=True)
    opacity = models.CharField(max_length=5, null=True)
    blend_mode = models.CharField(max_length=250, null=True)

    def __str__(self):
        return f"{self.name}"
