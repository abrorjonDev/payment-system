from django.db import models
from django.utils.translation import gettext_lazy as _

from payments.validators import deadline_validator


class CardTYPE(models.TextChoices):
    HUMO = 'humo', _('Humo')
    UZCARD = 'uzcard', _('Uzcard')
    VISA = 'visa', _('Visa')
    MASTER = 'mastercard', _('Mastercard')


class Card(models.Model):
    name = models.CharField(max_length=100)
    card_type = models.CharField(choices=CardTYPE.choices, max_length=10)
    number = models.CharField(max_length=16)
    deadline = models.CharField(max_length=5, validators=[deadline_validator])
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='cards')
    bank = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Card')
        verbose_name_plural = _('Cards')

    def __str__(self):
        return self.name


# class Transaction(models.Model): ...