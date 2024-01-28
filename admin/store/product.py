from django.contrib import admin , messages
from django.utils.safestring import mark_safe
from admin.store.inventory import InventoryFilter
from admin.store.productImage import ProductImageInline
from store.models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    actions = ['clear_inventory']
    inlines = [ProductImageInline]
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title', 'product_image']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 10
    # For optimizing query usage
    list_select_related = ['collection']
    search_fields = ['title']

    @mark_safe
    def product_image( self, obj ):
        if obj.images.exists():
            image_url = obj.images.first().image.url
            return f"<img src={image_url} height=120px width=120px />"
        return "No Image"


    # fieldsets = [
    #     (
    #         "Advanced options",
    #         {
    #             "classes": ['collapse'],
    #             "fields": ["title"]
    #         }
    #     )
    # ]

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.',
            messages.ERROR
        )

    # To load custom css , js
    class Media:
        css = {
            'all': ['store/style.css']
        }

