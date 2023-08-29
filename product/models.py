from django.db import models
from django.db import models
from django.urls import reverse
# from authors.models import author
from category.models import category
from django.utils.text import slugify
# Create your models here.


class Color(models.Model):
    color_name = models.CharField(max_length=50)
    color_code = models.CharField(max_length=15)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.color_name


class Product(models.Model):
    product_name = models.CharField(unique=True, max_length=50)
    product_price = models.IntegerField()
    category = models.ForeignKey(category, on_delete=models.CASCADE, default=3)
    product_image = models.ImageField(
        upload_to='photos/product', default='No image available')
    product_description = models.TextField(max_length=50, default="")
    is_available = models.BooleanField(default=True)

    # is_available = models.BooleanField(default=False)
    slug = models.SlugField(max_length=250, unique=True)
    # quantity = models.IntegerField(default=10)

    def save(self, *args, **kwargs):
        # generate slug field from name field if slug is empty
        if not self.slug:
            self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name


class ProductReview(models.Model):
    RATING_CHOICES = (
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    )

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    review_text = models.TextField()
    name = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    helpful_count = models.PositiveIntegerField(default=0)
