from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class Address(models.Model):
    """Model to store addresses for accounts"""
    address_line1 = models.CharField("Address line 1", max_length=45)
    address_line2 = models.CharField("Address line 2", max_length=45,
                                     blank=True)
    postal_code = models.CharField("Postal Code", max_length=10)
    city = models.CharField(max_length=50, blank=False)
    state_province = models.CharField("State/Province", max_length=40,
                                      blank=True)
    country = CountryField(default='US')
    user = models.ForeignKey(
        get_user_model(), blank=False, on_delete=models.PROTECT, related_name="user_address")

    def __str__(self):
        return "%s, %s %s" % (self.city, self.state_province,
                              str(self.country))

    class Meta:
        verbose_name_plural = "Addresses"
