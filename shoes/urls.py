from django.urls import path
from .views import (
    home, about,
    product_list, product_detail,
    cart_detail, cart_add, cart_remove, add_to_cart, update_quantity,
    order_create, order_detail, order_list,
    user_login, user_logout, register,
    SneakerDetail,
    add_review,
    update_order_status
)

urlpatterns = [
    # Основные страницы
    path('', home, name='home'),
    path('about/', about, name='about'),

    # Товары
    path('products/', product_list, name='product_list'),
    path('products/<slug:category_slug>/', product_list, name='product_list_by_category'),
    path('product/<int:id>/<slug:slug>/', product_detail, name='product_detail'),
    path('sneaker/<int:pk>/', SneakerDetail.as_view(), name='sneaker_detail'),

    # Корзина
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('add_to_cart/<str:model_type>/<int:model_id>/', add_to_cart, name='add_to_cart'),
    path('update-quantity/', update_quantity, name='update_quantity'),

    # Заказы
    path('order/create/', order_create, name='order_create'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),
    path('orders/', order_list, name='order_list'),
    path('order/<int:order_id>/update-status/', update_order_status, name='update_order_status'),

    # Аутентификация
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),

    # Отзывы
    path('product/<int:shoe_id>/review/', add_review, name='add_review'),
]