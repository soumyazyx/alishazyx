from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=255, blank=False)
    desc = models.TextField(blank=True)
    image = models.ImageField(blank=True, upload_to="images/categories/")
    sequence = models.IntegerField(blank=False, default=999)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ("sequence", "created_on")

    def __str__(self):
        return "{}. {}".format(self.sequence, self.name)


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sequence = models.IntegerField(blank=False, default=999)
    name = models.CharField(max_length=255, blank=False)
    desc = models.TextField(blank=True)
    image = models.ImageField(blank=True, upload_to="images/subcategories/")
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sub-Categories"
        ordering = ("category", "sequence", "created_on")

    def __str__(self):
        return "sequence={} / {} / {}".format(self.sequence, self.category.name, self.name)


class Product(models.Model):
    sku = models.CharField(max_length=255, blank=True, default="-1")
    title = models.CharField(max_length=255, blank=False)
    image = models.ImageField(blank=True, upload_to="images/products/")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, default=3)
    description = models.TextField(blank=True)
    cover_img_url = models.TextField(blank=True, null=True)
    product_img_urls_csv = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    additional_image_1 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_2 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_3 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_4 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_5 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_6 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_7 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_8 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_9 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_10 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_11 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_12 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_13 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_14 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_15 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_16 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_17 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_18 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_19 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_20 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_21 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_22 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_23 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_24 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_25 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_26 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_27 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_28 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_29 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_30 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_31 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_32 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_33 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_34 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_35 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_36 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_37 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_38 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_39 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_40 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_41 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_42 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_43 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_44 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_45 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_46 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_47 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_48 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_49 = models.ImageField(blank=True, null=True, upload_to="images/products/")
    additional_image_50 = models.ImageField(blank=True, null=True, upload_to="images/products/")

    class Meta:
        verbose_name_plural = "Products"
        ordering = ("-created_on",)

    def __str__(self):
        return "{} - {}".format(self.subcategory, self.title)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/products/")

    def __str__(self):
        return self.product.title

