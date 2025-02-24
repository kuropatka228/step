from django.urls import path
from. import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('product/', views.product, name='product'),
    path('sneaker/<int:pk>/', views.shoe_detail, name='sneaker_detail'),
    path('top_sneaker/<int:pk>/', views.shoe_detail, name='top_sneaker_detail'),
    path('shoe/<int:pk>/', views.shoe_detail, name='shoe_detail'),

]