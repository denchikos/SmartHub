from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404, HttpResponsePermanentRedirect
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from .models import Notebooks, NotebooksBrand, Laptop_images, Icons
from django.views.generic import DetailView

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


def Profile(request):
    return render(request, 'blance/Profile.html')


def notebooks(request):
    producer = request.GET.get('producer')
    if producer:
        items = Notebooks.objects.filter(Notebooks_brand__name__iexact=producer)
    else:
        items = Notebooks.objects.all()
    data_db = Notebooks.objects.all()
    data = {"title": "SmartHub",
            "menu": menu,
            }
    return render(request, 'blance/Notebooks.html', {'data_db': data_db, 'data': data, 'items': items})


def product_detail(request, id):
    db = Icons.objects.all()
    data_db = Laptop_images.objects.all()
    product = get_object_or_404(Notebooks, id=id),
    data = {
        "title": "SmartHub",
        "menu": "menu",
    }
    return render(request, 'blance/product_detail.html', {'product': product, 'data': data, 'data_db': data_db, "db": db})


class NewsDetailView(DetailView):
    model = NotebooksBrand
    template_name = 'ProductNotebooks.html'
    context_object_name = 'producer'
