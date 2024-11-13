from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=SmartHun.Status.PUBLISHED)


class SmartHun(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Чорновик'
        PUBLISHED = 1, 'Опубліковано'

    name = models.CharField(max_length=50)
    content = models.TextField(blank=True, null=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT)
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/', default=None, blank=True, null=True)
    objects = models.Manager()
    published = PublishedManager()


    def __str__(self):
        return self.name


class Notebooks(models.Model):
    name = models.CharField(max_length=50)
    content = models.TextField(null=True)
    rating = models.TextField(blank=True, null=True)
    price = models.TextField(blank=True, null=True)
    url_name = models.URLField()
    images = models.ImageField(null=True, max_length=200)
    Notebooks_brand = models.ManyToManyField('NotebooksBrand', blank=True)
    noteb_id = models.ForeignKey('NotebooksBrand', related_name='notebooksbrand_id',  on_delete=models.CASCADE)


class NotebooksBrand(models.Model):
    name = models.CharField(max_length=20)
    url_name = models.URLField()


class Laptop_images(models.Model):
    images_id = models.ForeignKey(Notebooks, related_name='images_id', on_delete=models.CASCADE)
    image_path = models.CharField(max_length=255)

class Icons(models.Model):
    image_path = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.image_path}"


class Laptop(models.Model):
    notebooks_id = models.ForeignKey(Notebooks, related_name='notebooks_id', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="Назва")

    # Основні характеристики
    series = models.CharField(max_length=100, verbose_name="Серія")

    # Екран
    screen_size = models.CharField(max_length=10, verbose_name="Діагональ екрану")
    screen_refresh_rate = models.CharField(max_length=10, verbose_name="Частота оновлення екрану")
    screen_type = models.CharField(max_length=50, verbose_name="Тип екрану")
    screen_resolution = models.CharField(max_length=20, verbose_name="Роздільна здатність")
    screen_coating = models.CharField(max_length=50, verbose_name="Покриття екрану")
    built_in_camera = models.CharField(max_length=50, verbose_name="Вбудована камера")

    # Процесор
    processor = models.CharField(max_length=100, verbose_name="Процесор")
    os = models.CharField(max_length=50, verbose_name="Операційна система")
    processor_generation = models.CharField(max_length=50, verbose_name="Покоління процесора")

    # Оперативна пам'ять
    ram_size = models.CharField(max_length=10, verbose_name="Обсяг оперативної пам'яті")
    ram_type = models.CharField(max_length=10, verbose_name="Тип оперативної пам'яті")
    ram_upgradeability = models.CharField(max_length=50, verbose_name="Можливість апгрейду")
    ram_characteristics = models.CharField(max_length=100, verbose_name="Характеристики оперативної пам'яті")

    # Накопичувачі даних
    ssd_size = models.CharField(max_length=10, verbose_name="Обсяг SSD")
    m2_slots = models.CharField(max_length=5, verbose_name="Кількість слотів M.2")
    ssd_interface = models.CharField(max_length=50, verbose_name="Стандарт інтерфейсу SSD M.2")
    storage_type = models.CharField(max_length=50, verbose_name="Тип накопичувача")

    # Відеокарта
    gpu_manufacturer = models.CharField(max_length=50, verbose_name="Виробник відеокарти")
    discrete_gpu = models.CharField(max_length=100, verbose_name="Дискретна відеокарта")
    gpu_memory = models.CharField(max_length=10, verbose_name="Обсяг пам'яті відеокарти")
    gpu_type = models.CharField(max_length=100, verbose_name="Тип відеокарти")
    integrated_gpu = models.CharField(max_length=100, verbose_name="Інтегрована відеокарта")

    # Корпус
    battery_capacity = models.CharField(max_length=10, verbose_name="Ємність акумулятора, Вт год")
    weight = models.CharField(max_length=5, verbose_name="Вага, кг")
    color = models.CharField(max_length=50, verbose_name="Колір")
    sound_system = models.TextField(verbose_name="Звукова система")
    manipulators = models.CharField(max_length=50, verbose_name="Маніпулятори")
    battery_characteristics = models.TextField(verbose_name="Характеристики батареї")
    dimensions = models.CharField(max_length=50, verbose_name="Габарити (Ш х Г х В)")

    # Підключення
    network_adapters = models.TextField(verbose_name="Мережеві адаптери")
    ports = models.TextField(verbose_name="Роз'єми та порти введення-виведення")

    def __str__(self):
        return self.series


class Comments(models.Model):
    laptops_id = models.ForeignKey(Laptop, related_name='images_id', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, verbose_name="ФІО")
    rating = models.TextField(blank=True, null=True, verbose_name="Оцінка")
    reviews_users = models.CharField(verbose_name="Відгук користувача")