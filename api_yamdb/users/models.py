from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    CHOICES = (
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user')
    )
    role = models.CharField(
        'Role',
        max_length=10,
        choices=CHOICES,
        blank=False,
        default=USER,
        null=False,
    )
    bio = models.TextField(
        'Biography',
        blank=True,
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
