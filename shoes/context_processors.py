from .models import Cart


def cart(request):
    cart = None
    cart_items = []
    cart_total = 0

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    elif 'cart_id' in request.session:
        cart_id = request.session.get('cart_id')
        cart = Cart.objects.filter(id=cart_id).first()

    if cart:
        cart_items = cart.items.all()
        cart_total = sum(item.get_total_price() for item in cart_items)

    return {
        'cart': cart,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_items_count': len(cart_items),
    }