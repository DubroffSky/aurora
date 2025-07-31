from django.contrib import admin
from aurora_store.models import Product, OrderItem, Order
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.detail import DetailView
from aurora_store.models import Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price']
    
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'created']
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'count']

