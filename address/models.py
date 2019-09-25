from django.db import models


class Country(models.Model):
    """Model for countries"""
    iso_code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=45, blank=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ["name", "iso_code"]


class StateProvince(models.Model):
    """Model for states and provinces"""
    iso_code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=55, blank=False)
    country = models.ForeignKey(
        Country, to_field="iso_code", on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "State or province"
        ordering = ["-country", "name"]


class Address(models.Model):
    """Model to store addresses for accounts"""
    address_line1 = models.CharField("Address line 1", max_length=45)
    address_line2 = models.CharField("Address line 2", max_length=45,
                                     blank=True)
    postal_code = models.CharField("Postal Code", max_length=10)
    city = models.CharField(max_length=50, blank=False)
    state_province = models.CharField("State/Province", max_length=40,
                                      blank=True)
    country = models.ForeignKey(Country, blank=False, on_delete=models.CASCADE)

    def __unicode__(self):
        return "%s, %s %s" % (self.city, self.state_province,
                              str(self.country))

    class Meta:
        verbose_name_plural = "Addresses"
        unique_together = ("address_line1", "address_line2", "postal_code",
                           "city", "state_province", "country")
