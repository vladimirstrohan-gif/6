from django.db import models
from .mixins import SlugMixin,ImageMixin
from django.conf import settings

class Category(SlugMixin,ImageMixin):
  name = models.CharField('Назва',max_length=100)

  class Meta:
    verbose_name = "Категорія"
    verbose_name_plural = "Категорії"
    #db_table = "categories"
    ordering =["-name"]


  def __str__(self):
    return self.name