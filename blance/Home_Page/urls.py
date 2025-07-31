from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', views.Home_page, name='home'),
    path('catalogue/', views.Catalogue, name='catalogue'),
    path('search/', views.Search, name='search'),
    path('order/', views.Order, name='order'),
    path('compare_the_list/', views.Compare_the_list, name='compare_the_list'),
    path('wish_list/', views.Wish_list, name='wish_list'),
    path('my_orders/', views.My_orders, name='my_orders'),
    path('computers/', views.computers, name='computers'),
    path('notebooks/', views.notebooks, name='notebooks'),
    path('notebooks/product/<int:id>/', views.product_detail, name='product_detail'),
    path('checkout/<int:id>/', views.checkout_view, name='checkout'),
    path('search-settlement/', views.search_settlement, name='search_settlement'),
    path('get-warehouses/', views.get_warehouses, name='get_warehouses'),
    path('characteristics/<int:laptop_id>/', views.characteristics, name='characteristics'),
    path('reviews/<int:comments_id>/', views.reviews, name='reviews'),
]
