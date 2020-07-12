from django.db import models
from django.utils import timezone


class Category(models.Model):
    # id = models.AutoField(primary_key=True) - added automatically
    name = models.CharField(max_length=255, blank=False)
    desc = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return "{} - {}".format(self.name, self.desc)


class Product(models.Model):
    product_sku = models.CharField(max_length=255, blank=True, default="-1")
    product_title = models.CharField(max_length=255, blank=False, unique=True)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_desription = models.TextField(blank=True)
    product_image = models.ImageField(blank=True, upload_to="images/")

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        return "{} - {} - {}".format(
            self.product_category, self.product_sku, self.product_title
        )
