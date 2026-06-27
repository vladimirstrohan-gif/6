from django.db import models
from django.conf import settings
from .product import Product

class Comment(models.Model):
  product = models.ForeignKey(
    Product, 
    on_delete=models.CASCADE, 
    related_name='comments'
    )
  author = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE, 
    related_name='comments'
    )
  comment = models.TextField('Коментар')
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name = 'Коментар'
    verbose_name_plural = 'Коментарі'
    ordering = ['-created_at']

  def __str__(self):
    return f"{self.author.username}: {self.comment[:30]}"
