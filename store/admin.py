from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'category', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    search_fields = ['name', 'description']

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'total']
    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'status', 'created_at', 'total_price']
    list_filter = ['status', 'created_at']
    search_fields = ['full_name', 'email']
    inlines = [OrderItemInline] 