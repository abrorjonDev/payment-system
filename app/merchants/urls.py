from django.urls import path, include


app_name = 'merchant'

urlpatterns = [
    path("api/", include("merchants.api.urls")),
]