from rest_framework.routers import DefaultRouter

from payments.api.viewsets import CardViewSet

router = DefaultRouter()
router.register("cards", CardViewSet, basename="cards")

app_name = 'api'

urlpatterns = [] + router.urls