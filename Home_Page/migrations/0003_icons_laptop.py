# Generated by Django 5.0.3 on 2024-09-30 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home_Page', '0002_remove_laptop_images_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Laptop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Назва')),
                ('series', models.CharField(max_length=100, verbose_name='Серія')),
                ('screen_size', models.CharField(max_length=10, verbose_name='Діагональ екрану')),
                ('screen_refresh_rate', models.CharField(max_length=10, verbose_name='Частота оновлення екрану')),
                ('screen_type', models.CharField(max_length=50, verbose_name='Тип екрану')),
                ('screen_resolution', models.CharField(max_length=20, verbose_name='Роздільна здатність')),
                ('screen_coating', models.CharField(max_length=50, verbose_name='Покриття екрану')),
                ('built_in_camera', models.CharField(max_length=50, verbose_name='Вбудована камера')),
                ('processor', models.CharField(max_length=100, verbose_name='Процесор')),
                ('os', models.CharField(max_length=50, verbose_name='Операційна система')),
                ('processor_generation', models.CharField(max_length=50, verbose_name='Покоління процесора')),
                ('ram_size', models.CharField(max_length=10, verbose_name="Обсяг оперативної пам'яті")),
                ('ram_type', models.CharField(max_length=10, verbose_name="Тип оперативної пам'яті")),
                ('ram_upgradeability', models.CharField(max_length=50, verbose_name='Можливість апгрейду')),
                ('ram_characteristics', models.CharField(max_length=100, verbose_name="Характеристики оперативної пам'яті")),
                ('ssd_size', models.CharField(max_length=10, verbose_name='Обсяг SSD')),
                ('m2_slots', models.CharField(max_length=5, verbose_name='Кількість слотів M.2')),
                ('ssd_interface', models.CharField(max_length=50, verbose_name='Стандарт інтерфейсу SSD M.2')),
                ('storage_type', models.CharField(max_length=50, verbose_name='Тип накопичувача')),
                ('gpu_manufacturer', models.CharField(max_length=50, verbose_name='Виробник відеокарти')),
                ('discrete_gpu', models.CharField(max_length=100, verbose_name='Дискретна відеокарта')),
                ('gpu_memory', models.CharField(max_length=10, verbose_name="Обсяг пам'яті відеокарти")),
                ('gpu_type', models.CharField(max_length=100, verbose_name='Тип відеокарти')),
                ('integrated_gpu', models.CharField(max_length=100, verbose_name='Інтегрована відеокарта')),
                ('battery_capacity', models.CharField(max_length=10, verbose_name='Ємність акумулятора, Вт год')),
                ('weight', models.CharField(max_length=5, verbose_name='Вага, кг')),
                ('color', models.CharField(max_length=50, verbose_name='Колір')),
                ('sound_system', models.TextField(verbose_name='Звукова система')),
                ('manipulators', models.CharField(max_length=50, verbose_name='Маніпулятори')),
                ('battery_characteristics', models.TextField(verbose_name='Характеристики батареї')),
                ('dimensions', models.CharField(max_length=50, verbose_name='Габарити (Ш х Г х В)')),
                ('network_adapters', models.TextField(verbose_name='Мережеві адаптери')),
                ('ports', models.TextField(verbose_name="Роз'єми та порти введення-виведення")),
            ],
        ),
    ]