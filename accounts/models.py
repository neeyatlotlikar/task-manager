from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager


class User(AbstractUser):
    ROLE_CHOICES: ClassVar = [
        ("admin", "Admin"),
        ("manager", "Manager"),
        ("member", "Member"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == "admin"
