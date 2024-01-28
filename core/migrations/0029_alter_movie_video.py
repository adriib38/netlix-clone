# Generated by Django 5.0 on 2024-01-28 11:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_alter_serie_cover_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='video',
            field=models.FileField(null=True, upload_to='movie_videos', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])]),
        ),
    ]
