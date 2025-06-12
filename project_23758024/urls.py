from django.contrib import admin
from django.urls import path, include
from .views import welcome_view, about_view, contacts_view

urlpatterns = [
    path('', include('alumni_app.urls')),
    path('about/', about_view, name='about'),
    path('contacts/', contacts_view, name='contacts'),
    path('admin/', admin.site.urls),
    path('welcome/', welcome_view, name='welcome'),
    path('auth/', include('alumni_management.urls')),
    path('', include('alumni_app.urls')), 
]
