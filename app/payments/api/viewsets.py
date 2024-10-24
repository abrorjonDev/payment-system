from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from payments.models import Card
from .serializers import (
    CardAddSerializer,
    CardSerializer,
    CardDetailsSerializer,
    VerifyCardSerializer,
)
from .services.card import CardService


class CardViewSet(ModelViewSet):
    """
    1. /check-card-details --> checks card details:
        - Is card connected to this phone_number?
        - What is owner name?
        - What is bank name?
    2. /add-card --> if checking process is valid,
                    would cache card details, and send otp to phone_number
    2. /verify_card_otp --> checks otp with phone_number, if valid, it would create card.
    4. list, retrieve, update methods work how they ve been written
    """

    serializer_class = CardSerializer
    def get_queryset(self):
        return Card.objects.filter(
            user=self.request.user
        )

    @swagger_auto_schema(
        request_body=CardDetailsSerializer,
    )
    @action(
        methods=['post'],
        detail=False,
        url_path='check-card-details',
        url_name='check-card-details'
    )
    def check_card_details(self, request, *args, **kwargs):
        serializer = CardDetailsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        card_service = CardService(
            number=serializer.validated_data['number'],
            deadline=serializer.validated_data['deadline'],
            phone_number=request.user.phone_number,
        )
        return Response(*card_service.card_details())

    @action(
        methods=['post'],
        detail=False,
        url_path='add-card',
        url_name='add-card'
    )
    def add_card(self, request, *args, **kwargs):
        serializer = CardAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        card_service = CardService(
            number=serializer.validated_data['number'],
            deadline=serializer.validated_data['deadline'],
            phone_number=request.user.phone_number,
            name=serializer.validated_data['name'],
        )
        return Response(*card_service.add_card())

    @action(
        methods=['post'],
        detail=False,
        url_path='card-otp-verify',
        url_name='card-otp-verify'
    )
    def verify_card_otp(self, request, *args, **kwargs):
        serializer = VerifyCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        card_service = CardService(
            number=serializer.validated_data['number'],
            deadline=serializer.validated_data['deadline'],
            phone_number=request.user.phone_number
        )

        try:
            data = card_service.verify(otp=serializer.validated_data['otp'])
        except KeyError:
            return Response({'message': 'otp expired'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({'message': 'otp invalid'}, status=status.HTTP_400_BAD_REQUEST)

        card = Card.objects.create(
            user=request.user,
            name=data['name'],
            card_type=data['card_type'],
            number=serializer.validated_data['number'],
            deadline=serializer.validated_data['deadline'],
            bank=data['bank'],
            created_at=timezone.now()
        )
        card_data = CardSerializer(card).data
        return Response(card_data, 201)

    def create(self, request, *args, **kwargs):
        return Response({"message": "Not Implemented"})
