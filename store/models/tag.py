from.mixins import SlugMixin
from django.db import models
from django.conf import settings

class Tag(SlugMixin):
  name = models.CharField('Назва', max_length=100, unique=True)

  def __str__(self):
    return self.name
  
class ProductTag(models.Model):
  product = models.ForeignKey('Product', on_delete=models.CASCADE)
  tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
  tagged_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
  tagged_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ('product','tag')

  def __str__(self):
    return f'{self.product} - {self.tag}'