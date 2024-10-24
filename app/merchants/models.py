from django.db import models
from django.utils.translation import gettext_lazy as _


class STATUS(models.TextChoices):
    ACTIVE = 'active', _("Active")
    SOON = 'soon', _("Soon") #  We are working on it, published as soon as possible.
    INACTIVE = 'inactive', _("Inactive") # Inactive service, not found in global search


class BaseModel(models.Model):
    status = models.CharField(choices=STATUS.choices, max_length=10, default=STATUS.INACTIVE)
    name_uz = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)

    class Meta:
        abstract = True


class MerchantCategory(BaseModel):
    icon = models.JSONField(default=dict)

    class Meta:
        verbose_name = _("Merchant Category")
        verbose_name_plural = _("Merchant Categories")

    def __str__(self):
        return self.name_uz or self.name_ru or self.name_en


class Merchant(BaseModel):
    image = models.ImageField(upload_to="images/merchants/", null=True, blank=True)
    category = models.ForeignKey('MerchantCategory', on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name="merchants")

    class Meta:
        verbose_name = _("Merchant")
        verbose_name_plural = _("Merchants")

    def __str__(self):
        return self.name_uz or self.name_ru or self.name_en


class MerchantField(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name="fields")
    # TODO: need to add labels for rendering in merchant payment page
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    required = models.BooleanField(default=False)

    class Meta:
        unique_together = (("merchant", "name"),)
        verbose_name = _("Merchant")
        verbose_name_plural = _("Merchants")
        indexes = [models.Index(fields=["merchant"])]
