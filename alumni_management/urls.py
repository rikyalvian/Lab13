"""
URL configuration for alumni_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from usermanagement.views_jwt import CustomTokenObtainPairView

schema_view = get_schema_view(
    openapi.Info(
        title="Alumni Management API",
        default_version='v1',
        description="Dokumentasi API Alumni Management",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="email@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('frontend_app_spa.urls')),
    path('auth/', include('usermanagement.urls')),
    # path('dashboard/', include('dashboard.urls')),
    # path('about/', include('about.urls')),
    # path('contacts/', include('contacts.urls')),
    path('api/', include('alumni_app.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
