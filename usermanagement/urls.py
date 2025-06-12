from django.urls import path
from .views import register, user_login, user_logout
from .views_api import UserRegisterAPIView, AlumniRegisterAPIView, UserRegisterWithAlumniAPIView

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('api/register/', UserRegisterAPIView.as_view(), name='api_register'),
    path('api/register-alumni/', AlumniRegisterAPIView.as_view(), name='api_register_alumni'),
    path('api/register-user-alumni/', UserRegisterWithAlumniAPIView.as_view(), name='api_register_user_alumni'),
]
