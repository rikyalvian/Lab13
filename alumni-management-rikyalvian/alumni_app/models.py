from django.db import models
from django.conf import settings

class Alumni(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='alumni_profile')
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    email = models.EmailField()
    graduation_year = models.IntegerField()
    major = models.CharField(max_length=100)
    job_position = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True)
    linkedin = models.URLField(blank=True)
    status_kerja = models.BooleanField(default=False)

    def __str__(self):
        return self.name
