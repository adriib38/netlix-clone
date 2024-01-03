# Generated by Django 5.0 on 2023-12-17 14:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_listcontent_movie_alter_listcontent_serie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listcontent',
            name='movie',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.movie'),
        ),
        migrations.AlterField(
            model_name='listcontent',
            name='serie',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.serie'),
        ),
    ]
