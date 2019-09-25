from django.db import models


class AddressModelMixin(models.Model):
    name = models.CharField("Full name", max_length=1024)
    address1 = models.CharField("Address line 1", max_length=1024)
    address2 = models.CharField(
        "Address line 2", max_length=1024, blank=True, null=True)
    zip_code = models.CharField("ZIP", max_length=12)
    city = models.CharField("City", max_length=1024)

    class Meta:
        abstract = True
