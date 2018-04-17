from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField()
    first_name = models.TextField()
    last_name = models.TextField()
