# Generated by Django 3.2.5 on 2021-07-18 22:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ads', '0002_auto_20210719_0052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ad',
            name='owner',
        ),
        migrations.AddField(
            model_name='ad',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]