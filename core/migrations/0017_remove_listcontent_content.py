# Generated by Django 5.0 on 2023-12-17 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_moviecontent_content_type_seriecontent_content_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listcontent',
            name='content',
        ),
    ]