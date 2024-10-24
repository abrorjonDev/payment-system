from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils.translation import gettext_lazy as _

from users.managers import UserManager


class Gender(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'
    OTHER = 'O', 'Other'


class User(AbstractUser):
    username = None
    phone_number = models.CharField(max_length=20, unique=True)
    phone_number2 = models.CharField(max_length=20, unique=True, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=Gender.choices, max_length=1, null=True, blank=True)
    image = models.ImageField(upload_to="images/profile/", null=True, blank=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = UserManager()


class Device(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='devices')
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Device')
        verbose_name_plural = _('Devices')
        indexes = [
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return self.name


class ActionLog(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='actions')
    action = models.CharField(max_length=500)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()

    class Meta:
        verbose_name = _('Action Log')
        verbose_name_plural = _('Action Logs')
        indexes = [
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return self.action


class SMS(models.Model):
    phone_number = models.CharField(max_length=20, unique=True)
    message = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = _('SMS')
        verbose_name_plural = _('SMSes')
        indexes = [models.Index(fields=['phone_number'])]


    def __str__(self):
        return f"{self.message[:40]}"
