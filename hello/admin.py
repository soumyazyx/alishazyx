from django.contrib import admin
from hello.models import Category, SubCategory, Product, ProductImage

admin.site.register(Category)
admin.site.register(SubCategory)


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]

    class Meta:
        model = Product


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass
