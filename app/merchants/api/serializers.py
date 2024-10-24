from rest_framework import serializers

from merchants.models import Merchant, MerchantCategory, MerchantField


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = '__all__'


class MerchantFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantField
        fields = '__all__'



class MerchantCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantCategory
        fields = '__all__'


class BaseReadSerializer(serializers.Serializer):
    status = serializers.CharField()
    name_uz = serializers.CharField()
    name_ru = serializers.CharField()
    name_en = serializers.CharField()


class MerchantFieldsReadOnlySerializer(serializers.Serializer):
    name = serializers.CharField()
    value = serializers.CharField()
    required = serializers.BooleanField()


class MerchantReadOnlySerializer(BaseReadSerializer):
    image = serializers.ImageField(allow_null=True, required=False)


class MerchantCategoryReadSerializer(BaseReadSerializer):
    icon = serializers.JSONField(allow_null=True)
    merchants = MerchantReadOnlySerializer(many=True, read_only=True)


class MerchantDetailSerializer(MerchantReadOnlySerializer):
    fields = MerchantFieldsReadOnlySerializer(many=True)
