from rest_framework.routers import DefaultRouter

from merchants.api.viewsets import (
    MerchantCategoryViewSet,
    MerchantViewSet,
    MerchantFieldViewSet,
)

router = DefaultRouter()
router.register("merchants/categories", MerchantCategoryViewSet, basename="merchant-categories")
router.register("merchants", MerchantViewSet, basename="merchants")
router.register("merchants/fields", MerchantFieldViewSet, basename="merchant-fields")

app_name = 'api'

urlpatterns = [] + router.urls
