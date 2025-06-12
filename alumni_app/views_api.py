from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Alumni
from .serializers import AlumniSerializer
from django.shortcuts import get_object_or_404

class AlumniListAPIView(APIView):
    def get(self, request):
        alumni = Alumni.objects.all()
        serializer = AlumniSerializer(alumni, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AlumniSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AlumniDetailAPIView(APIView):
    def get(self, request, pk):
        alumni = get_object_or_404(Alumni, pk=pk)
        serializer = AlumniSerializer(alumni)
        return Response(serializer.data)

    def put(self, request, pk):
        alumni = get_object_or_404(Alumni, pk=pk)
        serializer = AlumniSerializer(alumni, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        alumni = get_object_or_404(Alumni, pk=pk)
        alumni.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
