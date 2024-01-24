from django.contrib import admin
from django.utils.html import format_html
from store.models import ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ['thumbnail']
    extra = 1

    # To convert thumbnail and shows in admin
    def thumbnail( self, instance ):
        if instance.image.name != '':
            return format_html(f'<img src="{instance.image.url}" class="thumbnail"/>')
        return ""