# Generated by Django 5.0.3 on 2024-12-04 16:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home_Page', '0012_icons_laptop_processors'),
    ]

    operations = [
        migrations.AddField(
            model_name='laptop',
            name='laptop_processor_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='laptop_id', to='Home_Page.laptop_processors'),
            preserve_default=False,
        ),
    ]
