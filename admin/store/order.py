from django.contrib import admin
from store.models import Order
from admin.store.orderItem import OrderItemInline


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id', 'placed_at', 'customer']
    search_fields = ['customer__id']
    #! Fix the DisallowedModelAdminLookup Filtering by customer__id not allowed
    list_filter = ['customer']
