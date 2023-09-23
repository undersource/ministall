from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=50, unique=True, db_index=True)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

class Product(models.Model):
    product_file = models.FileField(upload_to='products')
    logo = models.ImageField(upload_to='logos')
    title = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=50, unique=True, db_index=True)
    description = models.CharField(max_length=200, db_index=True)
    price = models.DecimalField(max_digits=100, decimal_places=12)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})

    def get_file(self):
        return reverse('download', kwargs={'product_slug': self.slug})

class User(AbstractUser):
    monero_account_index = models.IntegerField(default=0)
    monero_address = models.TextField(max_length=95, default='0'*95)
    spent = models.DecimalField(max_digits=100, decimal_places=12, default=0)
    purchases = models.ManyToManyField(Product, blank=True)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.username