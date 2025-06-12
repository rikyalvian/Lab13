from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from alumni_app.models import Alumni  # Perbaiki import Alumni

class AlumniByYearAPIView(APIView):
    def get(self, request):
        alumni_by_year = Alumni.objects.values('graduation_year').annotate(count=Count('id')).order_by('graduation_year')
        data = {
            'labels': [str(item['graduation_year']) for item in alumni_by_year],
            'counts': [item['count'] for item in alumni_by_year]
        }
        return Response(data)
