from dataclasses import dataclass
from functools import lru_cache

from django.core.cache import cache

from users.api.services.auth import gen_otp
from payments.models import Card


CARDS = [
    {
        "number": "8600000000000000",
        "deadline": "10/26",
        "bank": "Xalqbank",
        "owner": "Firstname Lastname Middlename",
        "phone_number": "998971661186",
        "card_type": "uzcard"
    },
    {
        "number": "8600000000000001",
        "deadline": "09/25",
        "bank": "TBC",
        "owner": "Firstname Lastname Middlename",
        "phone_number": "998505051186",
        "card_type": "uzcard"
    },
    {
        "number": "8600000000000002",
        "deadline": "01/27",
        "bank": "Agrobank",
        "owner": "Firstname Lastname Middlename",
        "phone_number": "998971661186",
        "card_type": "uzcard"
    },
    {
        "number": "8600000000000003",
        "deadline": "10/23",
        "bank": "Infinbank",
        "owner": "Firstname Lastname Middlename",
        "phone_number": None,
        "card_type": "uzcard"
    }
]


@lru_cache
def filter_cards(number: str):
    return list(filter(lambda card: card["number"] == number, CARDS))


@dataclass
class CardService:
    number: str
    deadline: str
    phone_number: str # need for checking card owner is or not
    name: str = None
    bank: str = None
    owner: str = None
    card_type: str = None

    def card_details(self) -> tuple[dict, int]:
        cards = filter_cards(self.number)
        if not cards:
            return {
                "message": "card not found",
            }, 404
        if cards[0]["phone_number"] != self.phone_number:
            return {
                "message": "not_card_owner"
            }, 403

        return {
            "bank": cards[0]["bank"],
            "card_type": cards[0]["card_type"],
            "owner": cards[0]["owner"],
        }, 200

    def add_card(self) -> tuple[dict, int]:
        cards = filter_cards(self.number)
        if cards:
            if cards[0]["phone_number"] != self.phone_number:
                return {
                    "message": "not_card_owner"
                }, 403

            card_exists = Card.objects.filter(number=self.number).exists()
            if card_exists:
                return {
                    "message": "already added",
                }, 406

            otp = gen_otp()
            cache.set(f"card_add_{self.phone_number}", {
                "bank": cards[0]["bank"],
                "card_type": cards[0]["card_type"],
                "owner": cards[0]["owner"],
                "name": self.name,
                "otp": otp
            })

            # TODO: must send otp as sms message to connected phone_number
            return {
                "message": "otp sent",
                "otp": otp
            }, 200
        return {
            "message": "card not found"
        }, 400

    def verify(self, otp: int) -> dict | Exception:
        cache_key = f"card_add_{self.phone_number}"
        if not cache.has_key(cache_key):
            raise KeyError("otp expired")

        data = cache.get(cache_key)
        if data.get("otp") != otp:
            raise ValueError("otp invalid")

        return data
