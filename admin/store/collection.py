from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from store.models import Collection , Product
from django.utils.html import format_html, urlencode


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['featured_product']
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            }))
        return format_html('<a href="{}">{} Products</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )

    def save_model(self, request, obj, form, change):
        # Check for associated products only when saving the collection
        if 'featured_product' in form.changed_data:
            selected_products = form.cleaned_data['featured_product']
            associated_collections = Collection.objects.filter(featured_product__in=selected_products).exclude(pk=obj.pk)

            if associated_collections.exists():
                product = selected_products.first()  # Assuming you want to display information about the first associated product
                message = f"The product '{product}' is already associated with the following collection(s): {', '.join(map(str, associated_collections))}."
                self.message_user(request, message, level='warning')

        super().save_model(request, obj, form, change)

