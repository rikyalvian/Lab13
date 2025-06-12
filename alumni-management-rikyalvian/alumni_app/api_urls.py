from rest_framework.routers import DefaultRouter
from .views_drf import AlumniViewSet

router = DefaultRouter()
router.register(r'alumni', AlumniViewSet, basename='alumni')

urlpatterns = router.urls
