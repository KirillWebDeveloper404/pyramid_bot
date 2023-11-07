from django.db import models
from datetime import datetime


class User(models.Model):
    tg_id = models.TextField()

    class Meta:
        verbose_name = 'User'


class Messages(models.Model):
    address = models.TextField()
    text = models.TextField()

    class Meta:
        verbose_name = "Messages"
