from rest_framework.viewsets import ModelViewSet

from merchants.models import (
    Merchant,
    MerchantCategory,
    MerchantField
)
from .serializers import (
    MerchantSerializer, MerchantDetailSerializer,
    MerchantCategorySerializer, MerchantCategoryReadSerializer,
    MerchantFieldsSerializer
)


class SerializerMixin:
    read_serializer_class = None

    def get_serializer_class(self):
        if self.action in {'list', 'retrieve'}:

            assert self.read_serializer_class != None

            return self.read_serializer_class
        return self.serializer_class


class MerchantCategoryViewSet(SerializerMixin, ModelViewSet):
    queryset = MerchantCategory.objects.all()
    serializer_class = MerchantCategorySerializer
    read_serializer_class = MerchantCategoryReadSerializer
    filterset_fields = {
        'status': ['exact'],
        'name_uz': ['istartswith']  # TODO: must implement FilterSet class for i18n names filtering
    }


class MerchantViewSet(SerializerMixin, ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    read_serializer_class = MerchantDetailSerializer
    filterset_fields = {
        'category': ['exact'],
        'status': ['exact'],
        'name_uz': ['istartswith'] # TODO: must implement FilterSet class for i18n names filtering
    }

class MerchantFieldViewSet(SerializerMixin, ModelViewSet):
    queryset = MerchantField.objects.all()
    serializer_class = MerchantFieldsSerializer
    read_serializer_class = MerchantFieldsSerializer
    filterset_fields = {
        'merchant': ['exact'],
        'required': ['exact'],
    }
