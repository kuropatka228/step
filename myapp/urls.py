from django.urls import path
from. import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/', views.product, name='product'),
    path('cart/', views.cart, name='cart'),
    path('sneaker/<int:pk>/', views.SneakerDetail.as_view(), name='sneaker_detail'),
    path('add_to_cart/<str:model_type>/<int:model_id>/', views.add_to_cart, name='add_to_cart'),
]