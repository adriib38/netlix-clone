# Generated by Django 5.0 on 2023-12-17 15:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_content_alter_listcontent_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviecontent',
            name='list_content',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.listcontent'),
        ),
        migrations.AddField(
            model_name='seriecontent',
            name='list_content',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.listcontent'),
        ),
    ]