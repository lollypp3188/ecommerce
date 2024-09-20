from django.db import models
import uuid


class Category(models.Model):
  name = models.CharField(max_length=255, db_index=True)
  slug = models.SlugField(max_length=255, unique=True)
  id = models.UUIDField(
      default=uuid.uuid4, unique=True, primary_key=True, editable=False
  )

  class Meta:
    verbose_name_plural = 'categories'

  def __str__(self):
    return self.name


class Product(models.Model):
  title = models.CharField(max_length=255)
  brand = models.CharField(max_length=255, default='un-branded')
  description = models.TextField(blank=True)
  slug = models.SlugField(max_length=255)
  price = models.DecimalField(max_digits=4, decimal_places=2)
  image = models.ImageField(upload_to='images/')
  id = models.UUIDField(
      default=uuid.uuid4, unique=True, primary_key=True, editable=False
  )

  class Meta:
    verbose_name_plural = 'products'

  def __str__(self):
    return self.title
