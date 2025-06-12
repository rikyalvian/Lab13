from django.urls import path
from .views import dashboard_view
from .views_drf import AlumniByYearAPIView

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
]

urlpatterns += [
    # url APIView
    path('api/dashboard/by-year', AlumniByYearAPIView.as_view(), name='apiview_alumni_by_year'),
]
