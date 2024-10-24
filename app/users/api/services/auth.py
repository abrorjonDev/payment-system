import random

from enum import Enum
from django.core.cache import cache
from django.contrib.auth import get_user_model

gen_otp = lambda : random.randint(10000, 99990)

User = get_user_model()


class Action(Enum):
    REGISTER = 'reg'
    PASSWORD_RESET = 'pass_reset'


class AuthService:
    phone_number: str
    password: str
    action: Enum

    def __init__(
            self, phone_number: str, password: str=None,
            action: Action=Action.PASSWORD_RESET
    ):
        self.phone_number = phone_number
        self.password = password
        self.action = action

    def register(self):
        if cache.has_key(f"reg_{self.phone_number}"):
            cache.delete(f"reg_{self.phone_number}")

        otp = gen_otp()
        cache.set(f"reg_{self.phone_number}", {
            "otp": otp,
            "password": self.password
        })

        # TODO: Send otp in SMS Message

        return otp #  returns otp because of not sending sms

    def password_reset(self):
        if cache.has_key(f"pass_reset_{self.phone_number}"):
            cache.delete(f"pass_reset_{self.phone_number}")

        otp = gen_otp()
        cache.set(f"pass_reset_{self.phone_number}", {"otp": otp})

        # TODO: Send otp in SMS Message

        return otp

    def verify(self, otp):
        if self.action == Action.REGISTER:
            data = cache.get(f"reg_{self.phone_number}")
            if not data:
                raise KeyError
            elif data and data["otp"] != otp:
                return ValueError

            self.password = data.get("password")
            return True

        elif self.action == Action.PASSWORD_RESET:
            data = cache.get(f"pass_reset_{self.phone_number}")
            if not data:
                raise KeyError
            elif data and otp != data:
                raise ValueError

            return True

    def create_user(self):
        return User.objects.create_user(self.phone_number, password=self.password)