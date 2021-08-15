from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES = (
    ("admin", "admin"),
    ("moderator", "moderator"),
    ("guest", "guest"),
    ("user", "user")
)

class User(AbstractUser):
    role = models.CharField(
        "Роль",
        max_length=50,
        choices=CHOICES
    )
    bio = models.TextField(
        "Биография",
        blank=True,
    )