from django.db import models

from apps.users.models import User


class Category(models.Model):
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    icon_url = models.URLField(blank=True, null=True)

    class Meta:
        db_table = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    brand = models.CharField(max_length=255, blank=True, null=True)
    weight_grams = models.PositiveIntegerField(blank=True, null=True)
    flavor = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    discount_until = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "products"

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    is_main = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="products/")

    class Meta:
        db_table = "product_images"


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "reviews"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        db_table = "likes"
        unique_together = ("user", "product")


class Banner(models.Model):
    title = models.CharField(max_length=255)
    image_url = models.URLField()
    link_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "banners"
