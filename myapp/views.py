from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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
    try:
        model = Sneaker.objects.get(id=model_id)
    except Sneaker.DoesNotExist:
        messages.error(request, 'Product does not exist')
        return redirect('index')

    try:
        cart = Cart.objects.get(user=user, model_type=model_type, model_id=model_id)
        cart.quantity += 1
        cart.model_price = model.price
        cart.total_price = cart.model_price * cart.quantity
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=user, model_type=model_type, model_id=model_id, model_name=model.name, model_price=model.price, quantity=1, total_price=model.price)

    cart.save()
    return redirect('cart')

@login_required
def cart(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart:
        total_price += item.total_price
    return render(request, 'cart.html', {'cart': cart, 'total_price': total_price})