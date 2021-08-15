from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES = (
    ("admin", "admin"),
    ("moderator", "moderator"),
    ("user", "user")
)

class User(AbstractUser):

    role = models.CharField(
        "Роль",
        max_length=10,
        choices=CHOICES,
    )
    bio = models.TextField(
        "Биография",
        blank=True,
    )

    def __str__(self):
        return self.bio