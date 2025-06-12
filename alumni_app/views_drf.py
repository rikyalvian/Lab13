from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
try:
    from rest_framework.response import Response
except ImportError:
    pass
from .models import Alumni
from .serializers import AlumniSerializer
from usermanagement.permissions import IsOwnerOrReadOnly, IsAdmin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class AlumniViewSet(ModelViewSet):
    queryset = Alumni.objects.all()
    serializer_class = AlumniSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['major', 'graduation_year', 'job_position']
    search_fields = ['name', 'job_position']
    ordering_fields = ['name', 'graduation_year', 'company']
    ordering = ['name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        elif self.action == 'destroy':
            return [permissions.IsAuthenticated(), IsAdmin()]
        elif self.action in ['update', 'partial_update']:
            return [permissions.IsAuthenticated(), IsOwnerOrReadOnly()]
        elif self.action == 'create':
            return [permissions.IsAuthenticated(), IsAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        return Alumni.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()
        # Jangan paksa field user di update
        data.pop('user', None)
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
