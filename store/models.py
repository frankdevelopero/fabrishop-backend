from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fcm = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    state = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name + " - " + self.user.email


class Store(models.Model):
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='store', default='placeholder/store.png',
                              blank=True)
    whatsapp = models.TextField(blank=True, null=True)
    currency = models.CharField(max_length=20, default="$")
    address = models.TextField(blank=True, null=True)
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    state = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Category(models.Model):
    name = models.TextField()
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.BooleanField(default=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Product(models.Model):
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to='product', default='placeholder/product.png',
                              blank=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.BooleanField(default=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Gallery(models.Model):
    image = models.ImageField(upload_to='product', default='placeholder/product.png',
                              blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.image.url
