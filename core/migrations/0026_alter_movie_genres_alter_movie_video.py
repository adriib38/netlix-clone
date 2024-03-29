# Generated by Django 5.0 on 2024-01-21 11:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_alter_movie_genres'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(blank=True, to='core.genre'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='video',
            field=models.FileField(blank=True, default=3, upload_to='movie_videos', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])]),
            preserve_default=False,
        ),
    ]
