from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.TextField(verbose_name='name', null=True)
    phone = models.TextField(verbose_name='phone', null=True)

    class Meta:
        managed=True
        verbose_name = 'User'
        verbose_name_plural = 'Users'
