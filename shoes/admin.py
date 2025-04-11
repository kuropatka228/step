from django.contrib import admin
from .models import Category, Shoe, Review, Cart, CartItem, Order, OrderItem

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class ShoeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['shoe', 'author', 'rating', 'created', 'active']
    list_filter = ['active', 'created', 'rating']
    list_editable = ['active']
    search_fields = ['author', 'shoe__name', 'text']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['shoe']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'email', 'phone',
                    'address', 'city', 'paid', 'status', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated', 'status']
    inlines = [OrderItemInline]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Shoe, ShoeAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)