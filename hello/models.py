from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=255, blank=False)
    desc = models.TextField(blank=True)
    image = models.ImageField(blank=True, upload_to="images/categories/")
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return "{} - {}".format(self.name, self.desc)


class Product(models.Model):
    sku = models.CharField(max_length=255, blank=True, default="-1")
    title = models.CharField(max_length=255, blank=False, unique=True)
    image = models.ImageField(blank=True, upload_to="images/products/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    desription = models.CharField(max_length=255, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        return "{} - {}".format(self.category, self.title)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/products/")

    def __str__(self):
        return self.product.product_title
