# Generated by Django 3.2.15 on 2022-08-26 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recordings', '0009_notificationconfig'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recording',
            name='filepath',
            field=models.FilePathField(blank=True, null=True, path='/home/pi/birdnetlib-listener/recordings'),
        ),
    ]
