from django.db import models
from .mixins import SlugMixin
from .product import Product
from .attribute_value import AttributeValue

class Attribute(SlugMixin):
  name = models.CharField('Назва характеристики', max_length=100)

  class Meta:
    verbose_name = 'Характеристика'
    verbose_name_plural = 'Характеристики'

  def __str__(self):
    return self.name
  
class ProductAttribute(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
  attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE, related_name='products')

  class Meta:
    verbose_name = 'Характеристика товару'
    verbose_name_plural = 'Характеристики товарів'

  def __str__(self):
    return f"{self.product.name} - {self.attribute_value}"