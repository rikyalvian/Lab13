from django.urls import path
from .views import spa_index

urlpatterns = [
    path('', spa_index, name='spa_index'),
]
