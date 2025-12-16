from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home_page, name='home'),
    path('computers/', views.computers, name='computers'),
    path('notebooks/', views.notebooks, name='notebooks'),
    path('notebooks/product/<int:id>/', views.product_detail, name='product_detail'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('get-cart-items/', views.get_cart_items, name='get_cart_items'),
    path('search-settlement/', views.search_settlement, name='search_settlement'),
    path('get-warehouses/', views.get_warehouses, name='get_warehouses'),
    path('characteristics/<int:laptop_id>/', views.characteristics, name='characteristics'),
    path('reviews/<int:comments_id>/', views.reviews, name='reviews'),
    path('add-to-comparison/', views.add_to_comparison, name='add_to_comparison'),
    path('comparison/', views.compare_the_list, name='comparison'),
    #path('compare/', views.compare_list, name='compare_list'),
]
