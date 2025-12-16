from django.contrib import admin
#from .models import Notebooks, NotebooksBrand, Laptop_images, Laptop, Laptop_processors, Comments
#
#
#@admin.register(Notebooks)
#class NotebooksAdmin(admin.ModelAdmin):
#    list_display = ("name", "content", "rating", "price", "url_name", "images", "Notebooks_brand", "noteb_id",
#                    "processor_id")
#    search_fields = ("name", "content", "price", "Notebooks_brand", "noteb_id")
#
#
#@admin.register(NotebooksBrand)
#class NotebooksBrandAdmin(admin.ModelAdmin):
#    list_display = ("name", "url_name")
#    search_fields = "name"
#
#
#@admin.register(Laptop_images)
#class Laptop_imagesAdmin(Laptop_images):
#    list_display = ("images_id", "image_path")
#    search_fields = "images_id"
#
#
#@admin.register(Laptop)
#class LaptopAdmin(Laptop):
#    list_display = (
#        'id',
#        'name',
#        'series',
#        'processor',
#        'ram_size',
#        'ssd_size',
#        'gpu_manufacturer',
#        'discrete_gpu',
#        'screen_size',
#        'screen_resolution',
#        'os',
#        'color',
#        'weight',
#    )
#    list_filter = (
#        'processor',
#        'gpu_manufacturer',
#        'os',
#        'ram_size',
#        'color',
#    )
#    search_fields = (
#        'name',
#        'series',
#        'processor',
#        'discrete_gpu',
#        'os',
#    )
#
#
#@admin.register(Laptop_processors)
#class Laptop_processorsAdmin(admin.ModelAdmin):
#    list_display = "processor"
#
#
#@admin.register(Comments)
#class CommentsAdmin(admin.ModelAdmin):
#    list_display = ("laptops_id", "full_name", "rating", "reviews_users")
#    search_fields = ("laptops_id", "full_name", "rating", "reviews_users")


