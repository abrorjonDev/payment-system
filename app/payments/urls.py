from django.urls import path, include


app_name = 'payments'

urlpatterns = [
    path("api/", include("payments.api.urls")),
]