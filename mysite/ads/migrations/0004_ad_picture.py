# Generated by Django 3.2.5 on 2021-07-23 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0003_auto_20210719_0100'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]