from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from .views import home

from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger Schema View
schema_view = get_schema_view(
    openapi.Info(
        title="Social Hub API",
        default_version='v1',
        description="API documentation for Social Hub project",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[JWTAuthentication],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),  # Simple welcome route
    path("api/auth/", include("users.urls")),  # Include user-related routes
    path("api/posts/", include("posts.urls")),
    path("api/jobs/", include("jobs.urls")),
    path("api/events/", include("events.urls")),
    #  Swagger and ReDoc API docs
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

#  Media files handling in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
