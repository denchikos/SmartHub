# Generated by Django 5.0.3 on 2024-12-08 20:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home_Page', '0015_icons_laptop_processors_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notebooks',
            name='processor_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Home_Page.laptop_processors'),
            preserve_default=False,
        ),
    ]
