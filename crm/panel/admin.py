from django.contrib import admin
from .models import User, Invest, History


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'tg_id', 'balance']


@admin.register(Invest)
class InvestAdmin(admin.ModelAdmin):
    list_display = ['user', 'sum']


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'money', 'in_out', 'pay_id']


