from django.shortcuts import render, get_object_or_404, redirect
from .models import Notebooks, NotebooksBrand, Laptop_images, Laptop, Comments
from django.views.generic import DetailView
from django.db.models import Count
from urllib.parse import unquote
from random import sample
import requests
from django.http import JsonResponse


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


def notebooks(request):
    producer = request.GET.get('producer')
    min_price = request.GET.get('min')
    max_price = request.GET.get('max')
    processor = unquote(request.GET.get('processor', ''))
    search_query = request.GET.get('search', '')
    sort_option = request.GET.get('sort')

    items = Notebooks.objects.all()

    current_producers = producer.split(',') if producer else []

    if search_query:
        brands = NotebooksBrand.objects.values_list('name', flat=True)
        if search_query in brands:
            current_producers.append(search_query)

    if current_producers:
        items = items.filter(noteb_id__name__in=current_producers)

    if search_query and search_query not in current_producers:
        items = items.filter(name__icontains=search_query)

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

    current_processors = processor.split(',') if processor else []
    if current_processors:
        items = items.filter(processor_id__processor__in=current_processors)

    if sort_option == 'price_asc':
        items = items.order_by('price')
    elif sort_option == 'price_desc':
        items = items.order_by('-price')

    NotebooksBrand_count = NotebooksBrand.objects.count()
    brands_count = (Notebooks.objects.values('noteb_id__name').annotate(count=Count('id')).order_by('noteb_id__name'))
    processor_count = (Notebooks.objects.values('processor_id__processor').annotate(count=Count('id')))
    notebooks_count = items.count()

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


def compare_the_list(request):
    compare = request.session.get('compare', [])
    compare_len = len(compare)
    all_other_laptops = Laptop.objects.exclude(notebooks_id__in=compare)
    similar_products = sample(list(all_other_laptops), min(6, all_other_laptops.count()))
    similar_images = [Laptop_images.objects.filter(images_id=item.notebooks_id.id).first()
                      for item in similar_products
                      ]
    characteristic = {
        'Процесор': 'processor',
        'Покоління процесора': 'processor_generation',
        'Виробник відеокарти': 'gpu_manufacturer',
        'Тип відеокарти': 'gpu_type',
        'Ємність акумулятора': 'battery_capacity',
        'Вага': 'weight',
        'Колір': 'color',
        'Звукова система': 'sound_system',
        'Маніпулятори': 'manipulators',
        'Габарити (Ш х Г х В)': 'dimensions',
        'Обсяг SSD': 'ssd_size',
        'Кількість слотів M.2': 'm2_slots',
        'Тип накопичувача': 'storage_type',
        'Обсяг оперативної памяті': 'ram_size',
        'Тип оперативної памяті': 'ram_type',
        'Характеристики оперативної памяті': 'ram_characteristics',
        'Мережеві адаптери': 'network_adapters',
        'Діагональ екрану': 'screen_size',
        'Частота оновлення екрану': 'screen_refresh_rate',
        'Роздільна здатність': 'screen_resolution',
        'Тип екрану': 'screen_type',
        'Покриття екрану': 'screen_coating',
        'Вбудована камера': 'built_in_camera',
    }

    COLUMN_WIDTH = 276
    scroll_width = COLUMN_WIDTH * compare_len

    print("Товари у сесії:", compare)

    if not compare:
        return render(request, 'blance/comparison.html', {'products': []})

    products = Notebooks.objects.filter(id__in=compare)
    products_Laptop = Laptop.objects.filter(notebooks_id__in=compare)
    return render(request, 'blance/comparison.html', {
        'products': products,
        'products_Laptop': products_Laptop,
        'compare_len': compare_len,
        'similar_products_with_images': zip(similar_products, similar_images),
        'characteristic': characteristic,
        'scroll_width': scroll_width,
    })


def checkout_view(request):
    ids = request.GET.get("ids")
    if not ids:
        return redirect("home")

    ids = [i for i in ids.split(",") if i.isdigit()]
    if not ids:
        return redirect("home")

    if request.method == "POST":
        last_name = request.POST.get("last_name")
        first_name = request.POST.get("first_name")
        phone = request.POST.get("phone")
        delivery_method = request.POST.get("delivery_method")
        city = request.POST.get("city")
        warehouse = request.POST.get("warehouse")

        errors = []
        if not last_name or not first_name or not phone:
            errors.append("Усі обов’язкові поля мають бути заповнені.")
        if delivery_method == "np_warehouse" and (not city or not warehouse):
            errors.append("Оберіть місто та відділення.")

        if errors:
            return render(request, "checkout.html", {"errors": errors})

        return redirect("thank_you")

    products = Notebooks.objects.filter(id__in=ids)

    images = {}
    for product in products:
        main_image = Laptop_images.objects.filter(images_id=product.id).order_by("id").first()
        images[product.id] = main_image.image_path if main_image else None

    return render(request, "blance/checkout.html", {
        "products": products,
        "images": images,
    })


def get_cart_items(request):
    ids = request.GET.get("ids")
    if not ids:
        return JsonResponse({"items": []})

    ids = [i for i in ids.split(",") if i.strip().isdigit()]
    products = Notebooks.objects.filter(id__in=ids)
    data = []

    for product in products:
        image = Laptop_images.objects.filter(images_id=product.id).first()
        data.append({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "image": image.image_path if image else None,
        })

    return JsonResponse({"items": data})


def add_to_comparison(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')

        if product_id:
            compare = request.session.get('compare', [])

            if not isinstance(compare, list):
                compare = [str(compare)]

            added = False

            if product_id not in compare:
                compare.append(product_id)
                added = True
            else:
                compare.remove(product_id)

            request.session['compare'] = compare
            request.session.modified = True

            return JsonResponse({
                'status': 'ok',
                'added': added,
                'compare_count': len(compare)
            })

    return JsonResponse({'status': 'error'}, status=400)





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
    product = get_object_or_404(Notebooks, id=id)
    product = get_object_or_404(Notebooks, id=laptop_id)
    models = get_object_or_404(Laptop, id=laptop_id)
    models_laptop = Laptop.objects.get(id=laptop_id)
    return render(request, 'blance/characteristics.html', {'models': models, "product": product, 'models_laptop': models_laptop})


class NewsDetailView(DetailView):
    model = NotebooksBrand
    template_name = 'ProductNotebooks.html'
    context_object_name = 'producer'


def reviews(request, comments_id):
    models_laptop = get_object_or_404(Laptop, id=comments_id)
    models = get_object_or_404(Comments, id=comments_id)
    return render(request, 'blance/reviews.html', {'models': models, 'models_laptop': models_laptop})
