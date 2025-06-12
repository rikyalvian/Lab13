from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

# ✅ Model User Custom (untuk AUTH_USER_MODEL)
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_member = models.BooleanField(default=True)

    def __str__(self):
        return self.username

# ✅ Model Alumni
class Alumni(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='alumni_profiles'
    )

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    graduation_year = models.IntegerField()
    major = models.CharField(max_length=100)
    job_position = models.CharField(max_length=100)
    company = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)  # ✅ hanya ini
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Alumni'
        verbose_name_plural = 'Data Alumni'
        ordering = ['-graduation_year', 'name']

    def __str__(self):
        return self.name
