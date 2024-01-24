def product_image_upload_path(instance, filename):
    return f'store/images/productId_{instance.product.id}/{filename}'