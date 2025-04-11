from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q
from django.views.generic import DetailView
from .models import *
from .forms import *

class SneakerDetail(DetailView):
    model = Shoe
    template_name = 'product_detail.html'
    context_object_name = 'shoe'

def update_quantity(request):
    if request.method == 'POST' and request.is_ajax():
        item_id = request.POST.get('item_id')
        new_quantity = request.POST.get('quantity')
        try:
            cart_item = CartItem.objects.get(id=item_id)
            cart_item.quantity = new_quantity
            cart_item.save()
            return JsonResponse({'success': True})
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False})
    return JsonResponse({'success': False})

def add_to_cart(request, model_type, model_id):
    shoe = get_object_or_404(Shoe, id=model_id)
    cart = get_cart_for_request(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, shoe=shoe)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')

@login_required
def order_list(request):
    if request.user.is_superuser:
        orders = Order.objects.all().order_by('-created')
        return render(request, 'orders_admin.html', {
            'orders': orders,
            'status_choices': Order.STATUS_CHOICES
        })
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'orders_user.html', {'orders': orders})

@login_required
def update_order_status(request, order_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES).keys():
            order.status = new_status
            order.save()
            messages.success(request, f"Статус заказа #{order.id} обновлен")
        else:
            messages.error(request, "Неверный статус заказа")
    return redirect('order_list')

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if not request.user.is_superuser and order.user != request.user:
        return HttpResponseForbidden()
    template = 'orders_admin.html' if request.user.is_superuser else 'orders_user.html'
    context = {'order': order}
    if request.user.is_superuser:
        context.update({
            'orders': Order.objects.all().order_by('-created'),
            'status_choices': Order.STATUS_CHOICES,
            'single_order_view': True
        })
    return render(request, template, context)

def home(request):
    featured_shoes = Shoe.objects.filter(available=True).order_by('-created')[:8]
    reviews = Review.objects.filter(active=True).order_by('-created')[:3]
    show_review_form = False
    if request.user.is_authenticated and request.method == 'POST':
        if 'show_review_form' in request.POST:
            show_review_form = True
        elif 'submit_review' in request.POST:
            shoe_id = request.POST.get('shoe_id')
            shoe = get_object_or_404(Shoe, id=shoe_id)
            if not Review.objects.filter(shoe=shoe, user=request.user).exists():
                form = ReviewForm(request.POST)
                if form.is_valid():
                    review = form.save(commit=False)
                    review.shoe = shoe
                    review.user = request.user
                    review.author = request.user.username
                    review.save()
                    messages.success(request, "Ваш отзыв успешно добавлен!")
                    return redirect('home')
    return render(request, 'home.html', {
        'featured_shoes': featured_shoes,
        'reviews': reviews,
        'review_form': ReviewForm() if request.user.is_authenticated else None,
        'show_review_form': show_review_form,
    })

def about(request):
    return render(request, 'about.html', {'stats': {
        'customers': 12500, 'years': 5, 'products': 320, 'reviews': 8700
    }})

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    shoes = Shoe.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        shoes = shoes.filter(category=category)
    if query := request.GET.get('q'):
        shoes = shoes.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'products.html', {
        'category': category,
        'categories': categories,
        'shoes': shoes,
    })

def product_detail(request, id, slug):
    shoe = get_object_or_404(Shoe, id=id, slug=slug, available=True)
    related_shoes = Shoe.objects.filter(category=shoe.category, available=True).exclude(id=id)[:4]
    show_review_form = False
    user_review_exists = False
    form = None
    if request.user.is_authenticated:
        user_review_exists = Review.objects.filter(shoe=shoe, user=request.user).exists()
        if request.method == 'POST':
            if 'show_review_form' in request.POST:
                show_review_form = True
            elif 'submit_review' in request.POST:
                form = ReviewForm(request.POST)
                if form.is_valid():
                    review = form.save(commit=False)
                    review.shoe = shoe
                    review.user = request.user
                    review.author = request.user.username
                    review.save()
                    messages.success(request, "Ваш отзыв успешно добавлен!")
                    return redirect('product_detail', id=id, slug=slug)
        else:
            form = ReviewForm()
    return render(request, 'product_detail.html', {
        'shoe': shoe,
        'related_shoes': related_shoes,
        'reviews': shoe.reviews.filter(active=True).order_by('-created'),
        'review_form': form,
        'user_review_exists': user_review_exists,
        'can_add_review': request.user.is_authenticated and not user_review_exists,
        'show_review_form': show_review_form,
    })

def cart_detail(request):
    cart = get_cart_for_request(request)
    return render(request, 'cart.html', {'cart': cart if cart and cart.items.exists() else None})

def cart_add(request, product_id):
    shoe = get_object_or_404(Shoe, id=product_id)
    cart = get_cart_for_request(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, shoe=shoe)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{shoe.name} добавлен в корзину")
    return redirect('cart_detail')

def cart_remove(request, product_id):
    shoe = get_object_or_404(Shoe, id=product_id)
    cart = get_cart_for_request(request)
    if cart:
        cart_item = CartItem.objects.filter(cart=cart, shoe=shoe).first()
        if cart_item:
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
            messages.success(request, f"{shoe.name} удален из корзины")
    return redirect('cart_detail')

def add_review(request, shoe_id):
    if request.method == 'POST':
        shoe = get_object_or_404(Shoe, id=shoe_id)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.shoe = shoe
            review.author = request.user.username
            review.user = request.user
            review.save()
    return redirect('product_detail', id=shoe_id, slug=shoe.slug)

def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            cart = get_cart_for_request(request)
            if not cart or not cart.items.exists():
                messages.error(request, "Ваша корзина пуста")
                return redirect('cart_detail')
            order.save()
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    shoe=item.shoe,
                    price=item.shoe.price,
                    quantity=item.quantity,
                )
            cart.items.all().delete()
            if 'cart_id' in request.session:
                del request.session['cart_id']
            messages.success(request, "Ваш заказ успешно оформлен!")
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderForm()
    return render(request, 'order_create.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы")
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Добро пожаловать, {username}!")
                return redirect('home')
        messages.error(request, "Неверные имя пользователя или пароль")
    else:
        form = LoginForm(request)
    return render(request, 'login.html', {'form': form})

def get_cart_for_request(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get('cart_id')
        cart = Cart.objects.filter(id=cart_id).first() if cart_id else None
        if not cart:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
    return cart