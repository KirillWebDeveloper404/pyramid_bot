from django.db import models
from datetime import datetime


class User(models.Model):
    tg_id = models.TextField()
    balance = models.TextField(default=0)
    time_zone = models.TextField(default=0)
    referal = models.TextField(default=0)

    class Meta:
        verbose_name = 'User'


class Tariff(models.Model):
    name = models.TextField()
    procent = models.TextField()
    deadline = models.TextField()
    minimum = models.TextField()
    maximum = models.TextField()
    start_time = models.TextField()
    end_time = models.TextField()

    class Meta:
        verbose_name = 'Tariff'


class Invest(models.Model):
    name = models.TextField()
    user = models.TextField()
    procent = models.TextField()
    deadline = models.TextField()
    apply_out = models.TextField()
    sum = models.TextField()

    class Meta:
        verbose_name = 'Invest'


class History(models.Model):
    money = models.TextField()
    user = models.TextField()
    in_out = models.BooleanField()

    class Meta:
        verbose_name = 'History'


class MoneyOut(models.Model):
    money = models.TextField()
    user = models.TextField()
    card = models.TextField()

    class Meta:
        verbose_name = 'MoneyOut'


class Messages(models.Model):
    address = models.TextField()
    text = models.TextField()

    class Meta:
        verbose_name = "Messages"
