# Generated by Django 5.0.3 on 2024-10-28 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home_Page', '0006_icons_notebooksbrand_notebooks_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notebooksbrand',
            name='notebooks_id',
        ),
    ]
