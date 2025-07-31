from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import Notebooks, NotebooksBrand, Laptop_images, Icons, Laptop, Comments, Laptop_processors
from django.views.generic import DetailView
from django.conf import settings
from django.db.models import Count, Q
from urllib.parse import unquote
from random import sample
import requests
from django.http import JsonResponse
import time
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

API_KEY = 'b46aa1faf359401f1384419545e2f32d'


asorti = [{'id': 1, "title": 'Ноутбуки та компютери', 'url_name': 'computers',
           "images": 'Home_page/images/base_images/d1.jfif'},
          {'id': 2, "title": 'Смартфони, ТВ і електроніка', 'url_name': 'computers',
           "images": 'Home_page/images/base_images/завантаження.png'},
          {'id': 3, "title": 'Товари для геймерів', 'url_name': 'computers',
           "images": 'Home_page/images/base_images/завантаження.jfif'},
          {'id': 4, "title": 'Побутова техніка', 'url_name': 'computers',
           "images": 'Home_page/images/base_images/побутова_техніка.png'},
          {'id': 5, "title": 'Xiomi', 'url_name': 'computers',
           "images": 'Home_page/images/base_images/Xiaomi_logo.svg'},
          {'id': 6, "title": 'Apple', 'url_name': 'computers',
           "images": 'Home_page/images/base_images/391px-Apple_logo_black.svg.png'},
          ]

menu = [
    {"id": 1, 'title': 'Каталог', 'url_name': 'Catalogue'},
    {"id": 2, 'title': 'поиск', 'url_name': 'Search'},
    {"id": 3, 'title': 'замовлення', 'url_name': 'Order'},
    {"id": 4, 'title': 'Список порівняннь', 'url_name': 'Compare_the_list'},
    {"id": 5, 'title': 'Список бажаннь', 'url_name': 'Wish_list'},
    {"id": 6, 'title': 'Мої замовлення', 'url_name': 'My_orders'},
    {"id": 7, 'title': 'Профіль', 'url_name': 'Profile'},
]

data_computers = [
    {"id": 1, 'title': 'Ноутбуки', 'url_name': 'notebooks'},
    {"id": 2, 'title': 'Компютери', 'url_name': 'computers'},
    {"id": 3, 'title': 'Монітори', 'url_name': 'computers'},
    {"id": 4, 'title': 'планшети', 'url_name': 'computers'},
]

np_token_data = {
    "token": None,
    "expires": 0
}


def Home_page(request):
    data_db = Notebooks.objects.all()
    data = {"title": "SmartHub",
            "data_index": asorti,
            "menu": menu,
            }
    return render(request, 'blance/index.html', {'data_db': data_db, 'data': data})


def computers(request):
    data = {'title': "Комп'ютери та ноутбуки",
            'data': data_computers
            }
    return render(request, 'blance/laptops_and_computers.html', context=data)

def Catalogue(request):
    return HttpResponse('Каталог')


def Search(request):
    return HttpResponse('Пошук')


def Order(request):
    return HttpResponse('ваші замовлення')


def Compare_the_list(request):
    return HttpResponse('Список порівняннь')


def Wish_list(request):
    return HttpResponse('Список бажання')


def My_orders(request):
    return HttpResponse('ваші замовлення')


def notebooks(request):
    # Отримання параметрів запиту
    producer = request.GET.get('producer')  # Бренди
    min_price = request.GET.get('min')  # Мінімальна ціна
    max_price = request.GET.get('max')  # Максимальна ціна
    processor = unquote(request.GET.get('processor', ''))  # Процесори
    search_query = request.GET.get('search', '')  # Пошук
    sort_option = request.GET.get('sort')  # Сортування

    # Отримання всіх записів
    items = Notebooks.objects.all()

    # Фільтрація за брендами
    current_producers = producer.split(',') if producer else []

    # Якщо search_query є брендом, додаємо його до списку current_producers
    if search_query:
        brands = NotebooksBrand.objects.values_list('name', flat=True)  # Отримуємо список брендів із бази
        if search_query in brands:
            current_producers.append(search_query)

    if current_producers:
        items = items.filter(noteb_id__name__in=current_producers)

    # Фільтрація за пошуком
    if search_query and search_query not in current_producers:
        items = items.filter(name__icontains=search_query)

    # Фільтрація за ціною
    if min_price:
        try:
            items = items.filter(price__gte=int(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            items = items.filter(price__lte=int(max_price))
        except ValueError:
            pass

    # Фільтрація за процесорами
    current_processors = processor.split(',') if processor else []
    if current_processors:
        items = items.filter(processor_id__processor__in=current_processors)

    # Сортування
    if sort_option == 'price_asc':
        items = items.order_by('price')  # Від дешевих до дорогих
    elif sort_option == 'price_desc':
        items = items.order_by('-price')  # Від дорогих до дешевих

    # Збір додаткової інформації для відображення
    NotebooksBrand_count = NotebooksBrand.objects.count()
    brands_count = (Notebooks.objects.values('noteb_id__name').annotate(count=Count('id')).order_by('noteb_id__name'))
    processor_count = (Notebooks.objects.values('processor_id__processor').annotate(count=Count('id')))
    notebooks_count = items.count()

    # Підготовка контексту для шаблону
    data = {"title": "SmartHub", "menu": menu}
    return render(request, 'blance/Notebooks.html', {
        'data': data,
        'items': items,
        'notebooks_count': notebooks_count,
        'NotebooksBrand_count': NotebooksBrand_count,
        'brands_count': brands_count,
        'processor_count': processor_count,
        'current_producers': current_producers,
        'min_price': min_price,
        'max_price': max_price,
        'search_query': search_query,
    })


def product_detail(request, id):
    data_db = Laptop_images.objects.filter(images_id=id).order_by('id')
    product = get_object_or_404(Notebooks, id=id)
    models_laptop = Laptop.objects.get(notebooks_id=product)
    all_other_laptops = Laptop.objects.exclude(notebooks_id=product)
    similar_products = sample(list(all_other_laptops), min(6, all_other_laptops.count()))
    similar_images = [Laptop_images.objects.filter(images_id=item.notebooks_id.id).first()
                      for item in similar_products
                      ]
    main_image = Laptop_images.objects.filter(images_id=product).first()

    data = {
        "title": "SmartHub",
        "menu": menu,
    }
    return render(request, 'blance/product_detail.html', {
        'product': product,
        'data': data,
        'data_db': data_db,
        'models_laptop': models_laptop,
        'similar_products_with_images': zip(similar_products, similar_images),
        'main_image': main_image,
    })


def checkout_view(request, id):
    data_db = Laptop_images.objects.filter(images_id=id).order_by('id')
    product = get_object_or_404(Notebooks, id=id)
    models_laptop = Laptop.objects.get(notebooks_id=product)
    if request.method == "POST":
        last_name = request.POST.get("last_name")
        first_name = request.POST.get("first_name")
        phone = request.POST.get("phone")
        delivery_method = request.POST.get("delivery_method")
        city = request.POST.get("city")
        warehouse = request.POST.get("warehouse")

        # Простий приклад валідації:
        errors = []
        if not last_name or not first_name or not phone:
            errors.append("Усі обов’язкові поля мають бути заповнені.")
        if delivery_method == "np_warehouse" and (not city or not warehouse):
            errors.append("Оберіть місто та відділення.")

        if errors:
            return render(request, "checkout.html", {"errors": errors})

        # Тут можна створити модель Замовлення, зберегти її і перенаправити
        return redirect("thank_you")

    return render(request, "blance/checkout.html", {
        'data_db': data_db,
        'product': product,
        'models_laptop': models_laptop,
    })


def search_settlement(request):
    city = request.GET.get('query', '').strip()
    if not city:
        return JsonResponse([], safe=False)

    data = {
        "apiKey": API_KEY,
        "modelName": "Address",
        "calledMethod": "searchSettlements",
        "methodProperties": {
            "CityName": city,
            "Limit": 10
        }
    }

    response = requests.post("https://api.novaposhta.ua/v2.0/json/", json=data)
    settlements = []

    if response.status_code == 200 and response.json().get("success"):
        for address in response.json()["data"][0]["Addresses"]:
            settlements.append({
                "name": address["Present"],
                "ref": address["DeliveryCity"]
            })

    return JsonResponse(settlements, safe=False)


def get_warehouses(request):
    city_ref = request.GET.get("city_ref")
    if not city_ref:
        return JsonResponse([], safe=False)

    data = {
        "apiKey": API_KEY,
        "modelName": "Address",
        "calledMethod": "getWarehouses",
        "methodProperties": {
            "CityRef": city_ref,
            "Limit": 50
        }
    }

    response = requests.post("https://api.novaposhta.ua/v2.0/json/", json=data)
    warehouses = []

    if response.status_code == 200 and response.json().get("success"):
        for wh in response.json()["data"]:
            warehouses.append({
                "name": wh["Description"],
                "ref": wh["Ref"]
            })

    return JsonResponse(warehouses, safe=False)


def characteristics(request, laptop_id):
    #items = Notebooks.objects.all()
    product = get_object_or_404(Notebooks, id=laptop_id)
    models = get_object_or_404(Laptop, id=laptop_id)
    return render(request, 'blance/characteristics.html', {'models': models, "product": product})


class NewsDetailView(DetailView):
    model = NotebooksBrand
    template_name = 'ProductNotebooks.html'
    context_object_name = 'producer'


def reviews(request, comments_id):
    models_laptop = get_object_or_404(Laptop, id=comments_id)
    models = get_object_or_404(Comments, id=comments_id)
    return render(request, 'blance/reviews.html', {'models': models, 'models_laptop': models_laptop})


