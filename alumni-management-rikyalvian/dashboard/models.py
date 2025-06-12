from django.db import models
from django.conf import settings

class DashboardLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Menggunakan AUTH_USER_MODEL
    access_time = models.DateTimeField(auto_now_add=True)
    filters_used = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.access_time.strftime('%Y-%m-%d %H:%M:%S')}"