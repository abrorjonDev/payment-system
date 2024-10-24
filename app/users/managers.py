from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def _create_user(self, phone_number, is_staff, is_superuser, **extra_fields):
        if not phone_number:
            raise ValueError('unique phone_number must be required')

        password = extra_fields.pop('password', None)

        user = self.model(
            phone_number=phone_number,
            is_active=True,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, **extra_fields):
        return self._create_user(phone_number, False, False, **extra_fields)

    def create_superuser(self, phone_number, **extra_fields):
        return self._create_user(phone_number, True, True, **extra_fields)
