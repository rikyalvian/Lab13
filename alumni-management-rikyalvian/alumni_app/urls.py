from django.urls import path, include
# from .views import (
#     home,
#     about,
#     contacts,
#     dashboard,
#     alumni_profile,
#     AlumniListView,
#     AlumniDetailView,
#     AlumniCreateView,
#     AlumniUpdateView,
#     AlumniDeleteView,
#     alumni_detail_json
# )
from .views_api import AlumniListAPIView, AlumniDetailAPIView
from .api_urls import urlpatterns as api_urls

urlpatterns = [
    # Halaman Statis
    # path('', home, name='home'),
    # path('about/', about, name='about'),
    # path('contacts/', contacts, name='contacts'),

    # Dashboard & Profile
    # path('dashboard/', dashboard, name='dashboard'),
    # path('profile/', alumni_profile, name='alumni_profile'),
    # path('profile/<int:pk>/', AlumniDetailView.as_view(), name='profile'),

    # CRUD Alumni (untuk admin atau owner)
    # path('alumni/', AlumniListView.as_view(), name='list_alumni'),
    # path('alumni/add/', AlumniCreateView.as_view(), name='add_alumni'),
    # path('alumni/<int:pk>/', AlumniDetailView.as_view(), name='detail_alumni'),
    # path('alumni/<int:pk>/edit/', AlumniUpdateView.as_view(), name='update_alumni'),
    # path('alumni/<int:pk>/delete/', AlumniDeleteView.as_view(), name='delete_alumni'),

    # JSON View
    # path('alumni/<int:pk>/detail-json/', alumni_detail_json, name='alumni-detail-json'),
    # path('alumni/<int:pk>/detail/', alumni_detail_json, name='alumni-detail'),

    # Tambahkan ini agar DRF bisa berjalan
    # path('api/', include(api_urls)),
]

urlpatterns += api_urls
