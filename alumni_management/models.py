from django.contrib.auth.models import AbstractUser
from django.db import models

# Model untuk User, memperluas dari AbstractUser
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)  # Menandakan apakah user adalah admin
    is_member = models.BooleanField(default=True)  # Menandakan apakah user adalah alumni (member)

