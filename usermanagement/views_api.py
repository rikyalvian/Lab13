from rest_framework import generics, permissions
from .serializers import UserRegisterSerializer, AlumniRegisterSerializer, UserRegisterWithAlumniSerializer
from alumni_app.models import Alumni

class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

class AlumniRegisterAPIView(generics.CreateAPIView):
    serializer_class = AlumniRegisterSerializer
    queryset = Alumni.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserRegisterWithAlumniAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterWithAlumniSerializer
    permission_classes = [permissions.AllowAny]
