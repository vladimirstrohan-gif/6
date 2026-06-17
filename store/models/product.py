from django.db import models
from .mixins import SlugMixin,TimeMisin,ImageMixin
from .tag import Tag
  
class Product(SlugMixin,TimeMisin,ImageMixin):
  # tags = models.ManyToManyField(
  #   Tag,
  #   blank=True,
  #   verbose_name='Теги',
  #   related_name='products'
  #   )

  tags = models.ManyToManyField(
    Tag, 
    through='ProductTag',
    blank=True,
    verbose_name='Теги',
    related_name='products'
  )
  category = models.ForeignKey(
    'Category', 
    related_name='products',
    on_delete=models.SET_NULL,
    null=True,
    verbose_name='Категорія'
    )

  name = models.CharField('Назва',max_length=100)
  description = models.TextField('Опис',blank=True,null=True)
  price = models.DecimalField('Ціна',max_digits=10, decimal_places=2)
  sale_rpice = models.DecimalField('Ціна зі знижкою', max_digits=10,decimal_places=2,null=True,blank=True)
  stock = models.PositiveIntegerField('На складі',default=0)
  is_available = models.BooleanField('Доступний',default=True)
  total_price = models.DecimalField('Сума', max_digits=10, decimal_places=2,blank=True,null=True,editable=False)

  class Meta:
    verbose_name = 'Товар'
    verbose_name_plural = 'Товари'
    ordering = ['name']
    indexes = [
       models.Index(fields=['slug']),
       models.Index(fields=['category']),
       models.Index(fields=['is_available','stock'])
    ]
    constraints = [
      models.CheckConstraint(
        name='product_price_positive',
        condition=models.Q(price__gt=0) & models.Q(price__lt=99999999),
        violation_error_message="Ціна повинна бути від 0 до 9999999",
      ),
      models.CheckConstraint(
        name='product_stock_positive',
        condition=models.Q(price__gte=0),
        violation_error_message="Кількість товару повинна бути більше або дорівнювати 0",
      ),
    ]

  def save(self,*args,**kwargs):
    self.total_price = self.price*self.stock

    # is_new = self.pk is None
    # if is_new:
    #   print("Новий товар")

    super().save(*args,**kwargs)
  
  @property
  def available(self):
    return self.is_available and self.stock > 0
  
  @property
  def current_price(self):
    return self.sale_rpice if self.sale_rpice else self.price
  
  @property
  def is_on_sale(self):
    return self.sale_rpice is not None

  

  def __str__(self):
    return self.name