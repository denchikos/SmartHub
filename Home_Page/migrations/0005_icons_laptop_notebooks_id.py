# Generated by Django 5.0.3 on 2024-10-26 20:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home_Page', '0004_icons_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='laptop',
            name='notebooks_id',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='notebooks_id', to='Home_Page.notebooks'),
        ),
    ]
