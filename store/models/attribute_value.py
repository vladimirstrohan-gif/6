from django.db import models

class AttributeValue(models.Model):
  attribute = models.ForeignKey('Attribute', on_delete=models.CASCADE, related_name='values')
  value = models.CharField('Значення', max_length=100)

  class Meta:
    verbose_name = 'Значення характеристики'
    verbose_name_plural = 'Значення характеристик'

  def __str__(self):
    return f"{self.attribute.name}: {self.value}"