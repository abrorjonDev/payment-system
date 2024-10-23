from django.conf import settings

from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Payment System API",
      default_version='v1',
      description="Payment System Backend API docs",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="abrorjon.axmadov@outlook.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   path('admin/', admin.site.urls),
   path('swagger<format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('docs', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
   urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)