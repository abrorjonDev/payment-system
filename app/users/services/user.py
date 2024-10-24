from django.contrib.auth import get_user_model

User = get_user_model()


class UserService:
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone_number: str
    password: str
    phone_number2: str
    birthdate: str
    gender: str