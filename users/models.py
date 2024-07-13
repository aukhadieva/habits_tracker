from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="эл. почта")

    tg_chat_id = models.CharField(max_length=50, verbose_name="телеграм chat-id")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
