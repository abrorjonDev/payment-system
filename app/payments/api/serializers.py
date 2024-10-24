from rest_framework import serializers

from payments.models import Card


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = (
            'id', 'name', 'card_type', 'number', 'deadline', 'bank', 'created_at'
        )


class CardDetailsSerializer(serializers.Serializer):
    number = serializers.CharField()
    deadline = serializers.CharField()


class CardAddSerializer(CardDetailsSerializer):
    name = serializers.CharField()


class VerifyCardSerializer(serializers.ModelSerializer):
    otp = serializers.IntegerField(write_only=True)
    class Meta:
        model = Card
        fields = ("number", "deadline", "otp")