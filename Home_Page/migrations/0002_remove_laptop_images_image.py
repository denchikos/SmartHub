# Generated by Django 5.0.3 on 2024-08-23 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Home_Page', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='laptop_images',
            name='image',
        ),
    ]
