# Generated by Django 4.1.2 on 2022-10-30 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='slug',
            field=models.CharField(max_length=1000, null=True, unique=True),
        ),
    ]
