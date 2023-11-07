# Generated by Django 3.2.8 on 2022-12-05 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tilda', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tildaarticle',
            name='archive',
            field=models.FileField(blank=True, null=True, upload_to='tilda/zip/', verbose_name='Импорт из файла'),
        ),
        migrations.AlterField(
            model_name='tildaarticle',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='tildaarticle',
            name='tilda_content',
            field=models.TextField(blank=True, verbose_name='HTML-код'),
        ),
    ]
