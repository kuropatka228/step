from django.shortcuts import render, redirect
from django.views import generic
from.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json


def index(request):
    top_sneaker_categories = TopSneakerCategory.objects.all()
    return render(request, 'base.html', {'top_sneaker_categories': top_sneaker_categories})

class SneakerDetail(generic.DetailView):
    model = Sneaker
    template_name ='shoe_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shoe'] = self.object
        return context

def product(request):
    sneakers = Sneaker.objects.all()
    collections = SneakerCollection.objects.all()
    return render(request, 'product.html', {'sneakers': sneakers, 'collections': collections})

def shoe_detail(request, pk):
    shoe = Sneaker.objects.get(pk=pk)
    return render(request,'shoe_detail.html', {'shoe': shoe})

@login_required
def add_to_cart(request, model_type, model_id):
    user = request.user
    sneaker = Sneaker.objects.get(id=model_id)
    cart, created = Cart.objects.get_or_create(user=user, sneaker=sneaker)
    if not created:
        cart.quantity += 1
        cart.total_price = cart.quantity * sneaker.price
        cart.save()
    return redirect('cart')

@login_required
def cart(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart:
        total_price += item.total_price
    return render(request, 'cart.html', {'cart': cart, 'total_price': total_price})


@csrf_exempt
@require_POST
@login_required
def update_quantity(request):
    try:
        data = json.loads(request.body)  # JSON вместо request.POST
        item_id = data.get('item_id')
        quantity = int(data.get('quantity'))

        cart_item = Cart.objects.get(id=item_id, user=request.user)  # Проверка пользователя
        cart_item.quantity = quantity
        cart_item.save()

        return JsonResponse({'success': True, 'new_total_price': cart_item.total_price})

    except Cart.DoesNotExist:
        return JsonResponse({'error': 'Товар не найден в корзине'})
    except Exception as e:
        return JsonResponse({'error': str(e)})


def add_to_cart(request, model_type, model_id):
    user = request.user
    sneaker = Sneaker.objects.get(id=model_id)
    try:
        cart_item = Cart.objects.get(user=user, sneaker=sneaker)
        cart_item.quantity += 1
        cart_item.save()
    except Cart.DoesNotExist:
        Cart.objects.create(user=user, sneaker=sneaker, quantity=1)
    return redirect('cart')



