from django.shortcuts import render
from.models import *

def index(request):
    top_sneaker_categories = TopSneakerCategory.objects.all()
    return render(request, 'base.html', {'top_sneaker_categories': top_sneaker_categories})

def product(request):
    sneakers = Sneaker.objects.all()
    return render(request, 'product.html', {'sneakers': sneakers})
